from rank_bm25 import BM25Okapi
from langchain_core.documents import Document


def build_bm25_index(vector_store):

    chroma_data = vector_store.get(include=["documents", "metadatas"])

    documents = [
        Document(
            page_content=document,
            metadata=metadata,
        )
        for document, metadata in zip(
            chroma_data["documents"],
            chroma_data["metadatas"],
        )
    ]

    tokenized_documents = [
        document.page_content.lower().split() for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    return bm25, documents
