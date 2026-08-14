from sentence_transformers import CrossEncoder

# RERANKER_MODEL = "BAAI/bge-reranker-v2-m3" # heavey one
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"  # chepaer and light

reranker = CrossEncoder(RERANKER_MODEL)


def rerank_documents(
    question: str,
    documents,
    top_n: int = 3,
):

    pairs = [(question, document.page_content) for document in documents]

    scores = reranker.predict(pairs)

    ranked_documents = sorted(
        zip(documents, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked_documents[:top_n]
