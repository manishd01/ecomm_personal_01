import os
import time
from app.query_rewriter import rewrite_query

from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from app.reranker import rerank_documents

from dotenv import load_dotenv

from app.bm25 import build_bm25_index

load_dotenv()


CHROMA_DIR = "/app/data/chroma"
COLLECTION_NAME = "ecommerce_knowledge"


# --------------------------------------------------
# Load embedding model ONCE
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu",
    },
    encode_kwargs={
        "normalize_embeddings": True,
    },
)


# --------------------------------------------------
# Create Chroma connection ONCE
# --------------------------------------------------

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)

bm25, bm25_documents = build_bm25_index(vector_store)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.environ["GEMINI_API_KEY"],
)


def bm25_search(question: str, k: int = 10):
    print(f"BM25 search for: {question}")
    tokenized_query = question.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True,
    )[:k]

    return [bm25_documents[i] for i in ranked_indexes]


def retrieve_documents(
    question: str,
    k: int = 6,
):

    results = vector_store.similarity_search_with_score(
        question,
        k=k,
    )

    return [document for document, score in results]


def generate_answer(question: str, documents):

    context = "\n\n".join(document.page_content for document in documents)

    prompt = f"""
You are an AI assistant for an e-commerce platform.

Answer the customer's question using ONLY the provided
company knowledge.

If the knowledge does not contain enough information,
say that you do not have enough information.

Do not invent policies.

Company knowledge:

{context}

Customer question:

{question}
"""

    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-3.5-flash-lite",
    # )
    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-3.5-flash-lite",
    #     google_api_key=os.environ["GEMINI_API_KEY"],
    # )

    # response = llm.invoke(prompt)
    # response = llm.invoke(prompt)

    # if isinstance(response.content, list):
    #     answer = "".join(
    #         item.get("text", "") for item in response.content if isinstance(item, dict)
    #     )
    # else:
    #     answer = response.content

    for chunk in llm.stream(prompt):

        if isinstance(chunk.content, list):

            text = "".join(
                item.get("text", "") for item in chunk.content if isinstance(item, dict)
            )

        else:

            text = chunk.content

        if text:
            yield text

    # return answer


def reciprocal_rank_fusion(
    result_lists,
    k: int = 60,
):
    scores = {}
    documents = {}

    for results in result_lists:
        for rank, document in enumerate(results, start=1):

            doc_id = document.metadata.get("source", "") + document.page_content

            rrf_score = 1 / (k + rank)

            scores[doc_id] = scores.get(doc_id, 0) + rrf_score
            documents[doc_id] = document

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [documents[doc_id] for doc_id, score in ranked]


def answer_question(question: str):
    start_time = time.perf_counter()

    print(f"\nQUESTION: {question}")

    # 1. Query rewriting
    start = time.perf_counter()

    search_query = rewrite_query(question)
    # search_query = question

    print(f"Original query: {question}")
    print(f"Rewritten query: {search_query}")
    print(f"QUERY REWRITE TIME: {time.perf_counter() - start:.2f}s")

    # 2. Dense vector retrieval
    start = time.perf_counter()

    vector_candidates = retrieve_documents(
        search_query,
        k=10,
    )

    print(f"VECTOR RESULTS: {len(vector_candidates)}")
    print(f"VECTOR SEARCH TIME: {time.perf_counter() - start:.2f}s")

    # 3. Lexical BM25 retrieval
    start = time.perf_counter()

    bm25_candidates = bm25_search(
        search_query,
        k=10,
    )

    print(f"BM25 RESULTS: {len(bm25_candidates)}")
    print(f"BM25 SEARCH TIME: {time.perf_counter() - start:.2f}s")

    # 4. Combine both rankings
    start = time.perf_counter()

    candidates = reciprocal_rank_fusion(
        [
            vector_candidates,
            bm25_candidates,
        ]
    )

    print(f"RRF RESULTS: {len(candidates)}")
    print(f"RRF TIME: {time.perf_counter() - start:.2f}s")

    # 5. CrossEncoder reranking
    start = time.perf_counter()

    ranked_documents = rerank_documents(
        question,
        candidates[:20],
        top_n=3,
    )

    print(f"RERANKER RESULTS: {len(ranked_documents)}")
    print(f"RERANKER TIME: {time.perf_counter() - start:.2f}s")

    relevant_documents = [document for document, score in ranked_documents]

    # 6. LLM generation
    start = time.perf_counter()

    # answer = generate_answer(
    #     question,
    #     relevant_documents,
    # )

    # print(f"LLM GENERATION TIME: {time.perf_counter() - start:.2f}s")

    # # Total request time
    # total_time = time.perf_counter() - start_time

    # print(f"TOTAL TIME: {total_time:.2f}s")

    # return {
    #     "answer": answer,
    #     "sources": [document.metadata for document in relevant_documents],
    # }

    for chunk in generate_answer(
        question,
        relevant_documents,
    ):
        yield chunk

    print(f"LLM GENERATION TIME: {time.perf_counter() - start:.2f}s")

    total_time = time.perf_counter() - start_time

    print(f"TOTAL TIME: {total_time:.2f}s")


# //how to get my order money back?
