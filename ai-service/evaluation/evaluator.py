import json
from pathlib import Path

from pydantic import BaseModel, Field
from app.rag import retrieve_relevant_documents


class EvaluationSample(BaseModel):
    id: str
    question: str
    reference_answer: str
    relevant_sources: list[str] = Field(default_factory=list)
    expected: str


class EvaluationDataset(BaseModel):
    samples: list[EvaluationSample]


def load_evaluation_dataset(path: str) -> EvaluationDataset:
    dataset_path = Path(path)

    with dataset_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return EvaluationDataset(samples=data)


def get_retrieved_sources(question: str, top_k: int = 3) -> list[str]:
    """
    Run the actual RAG retrieval pipeline and
    return the source filenames of the top-k documents.
    """

    ranked_documents = retrieve_relevant_documents(
        question,
        top_n=top_k,
    )

    sources = [
        document.metadata.get("source", "") for document, score in ranked_documents
    ]

    return sources


def get_retrieved_sources(question: str, top_k: int = 3) -> list[str]:
    """
    Run the actual RAG retrieval pipeline and
    return the source filenames of the top-k documents.
    """

    ranked_documents = retrieve_relevant_documents(
        question,
        top_n=top_k,
    )

    sources = [
        document.metadata.get("source", "") for document, score in ranked_documents
    ]

    return sources


# 🟢 NEW
def calculate_recall_at_k(
    retrieved_sources: list[str],
    relevant_sources: list[str],
) -> float:

    if not relevant_sources:
        return 0.0

    retrieved = set(retrieved_sources)
    relevant = set(relevant_sources)

    hits = retrieved.intersection(relevant)

    return len(hits) / len(relevant)


# 🟢 NEW
def calculate_precision_at_k(
    retrieved_sources: list[str],
    relevant_sources: list[str],
) -> float:

    if not retrieved_sources:
        return 0.0

    retrieved = set(retrieved_sources)
    relevant = set(relevant_sources)

    hits = retrieved.intersection(relevant)

    return len(hits) / len(retrieved_sources)


if __name__ == "__main__":
    dataset_path = Path(__file__).parent / "datasets" / "rag_eval.json"

    dataset = load_evaluation_dataset(dataset_path)

    print(f"Loaded {len(dataset.samples)} evaluation samples")

    TOP_K = 3

    total_recall = 0.0
    total_precision = 0.0

    for sample in dataset.samples:

        retrieved_sources = get_retrieved_sources(
            sample.question,
            top_k=TOP_K,
        )

        recall = calculate_recall_at_k(
            retrieved_sources,
            sample.relevant_sources,
        )

        precision = calculate_precision_at_k(
            retrieved_sources,
            sample.relevant_sources,
        )

        total_recall += recall
        total_precision += precision

        print(f"\nID: {sample.id}")
        print(f"Question: {sample.question}")
        print(f"Expected sources: {sample.relevant_sources}")
        print(f"Retrieved sources: {retrieved_sources}")
        print(f"Recall@{TOP_K}: {recall:.3f}")
        print(f"Precision@{TOP_K}: {precision:.3f}")

    sample_count = len(dataset.samples)

    average_recall = total_recall / sample_count
    average_precision = total_precision / sample_count

    print("\n" + "=" * 50)
    print("RETRIEVAL EVALUATION")
    print("=" * 50)

    print(f"Samples: {sample_count}")
    print(f"Recall@{TOP_K}: {average_recall:.3f}")
    print(f"Precision@{TOP_K}: {average_precision:.3f}")
