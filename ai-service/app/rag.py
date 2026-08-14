from langchain_chroma import Chroma
from app.reranker import rerank_documents  # for ranking the reranker file..

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()


CHROMA_DIR = "/app/data/chroma"
COLLECTION_NAME = "ecommerce_knowledge"


def get_vector_store():

    # LOCAL EMBEDDING MODEL
    # No Gemini API call happens here.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def retrieve_documents(
    question: str,
    k: int = 6,
):

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        question,
        k=k,
    )

    # here we are getting, first n element from what we got from. in prev step . (not reranker)...

    return [document for document, score in results]


# def rerank_documents(

# question: str,

# documents,

# top_n: int = 3,

# ):

# """

# Initial reranking stage.

# We retrieve more candidates first and then keep

# the strongest candidates for the LLM.

# """

# return documents[:top_n]

# with reranker:


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
    #     model="gemini-3.6-flash",
    # )   #expesive:

    # cheap model:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
    )

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        answer = "".join(
            item.get("text", "") for item in response.content if isinstance(item, dict)
        )
    else:
        answer = response.content

    return answer


def answer_question(question: str):

    candidates = retrieve_documents(
        question,
        k=6,
    )

    ranked_documents = rerank_documents(
        question,
        candidates,
        top_n=3,
    )

    relevant_documents = [document for document, score in ranked_documents]

    answer = generate_answer(
        question,
        relevant_documents,
    )

    return {
        "answer": answer,
        "sources": [document.metadata for document in relevant_documents],
    }
