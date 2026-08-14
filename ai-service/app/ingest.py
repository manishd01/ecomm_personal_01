from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


KNOWLEDGE_DIR = Path("/app/knowledge")
CHROMA_DIR = "/app/data/chroma"

COLLECTION_NAME = "ecommerce_knowledge"


def load_document(file_path: Path) -> Document:
    content = file_path.read_text(encoding="utf-8")

    return Document(
        page_content=content,
        metadata={
            "source": file_path.name,
            "document_type": "knowledge",
        },
    )


def split_document(document: Document) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents([document])

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    return chunks


def create_vector_store() -> Chroma:

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    return vector_store


def ingest_file(file_path: Path):

    print(f"Starting ingestion for: {file_path.name}", flush=True)

    # -----------------------------------------
    # 1. Load ONLY this document
    # -----------------------------------------

    document = load_document(file_path)

    print(
        f"Loaded document: {file_path.name}",
        flush=True,
    )

    # -----------------------------------------
    # 2. Split ONLY this document
    # -----------------------------------------

    chunks = split_document(document)

    print(
        f"Created {len(chunks)} chunks for {file_path.name}",
        flush=True,
    )

    # -----------------------------------------
    # 3. Connect to Chroma
    # -----------------------------------------

    vector_store = create_vector_store()

    # -----------------------------------------
    # 4. Delete OLD chunks for this document
    # -----------------------------------------

    source = file_path.name

    existing = vector_store.get(where={"source": source})

    if existing["ids"]:

        vector_store.delete(ids=existing["ids"])

        print(
            f"Deleted {len(existing['ids'])} old chunks " f"for {source}",
            flush=True,
        )

    # -----------------------------------------
    # 5. Add NEW chunks
    # -----------------------------------------

    ids = [f"{source}:{chunk.metadata['chunk_id']}" for chunk in chunks]

    vector_store.add_documents(
        documents=chunks,
        ids=ids,
    )

    print(
        f"Added {len(chunks)} new chunks for {source}",
        flush=True,
    )

    print(
        f"Incremental ingestion completed: {source}",
        flush=True,
    )


def ingest_knowledge():

    print(
        "Running full knowledge ingestion...",
        flush=True,
    )

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        ingest_file(file_path)

    print(
        "Full RAG ingestion completed successfully.",
        flush=True,
    )


if __name__ == "__main__":
    ingest_knowledge()
