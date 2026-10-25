
import csv
import json
from pathlib import Path

from amanara.rag.retriever import Retriever


EVALUATION_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVALUATION_DIR / "test_dataset.json"
RESULTS_PATH = EVALUATION_DIR / "retrieval_results.csv"
TOP_K = 5


def evaluate_question(retriever, test_case):
    question = test_case["question"]
    relevant_ids = set(test_case["relevant_point_ids"])
    answerable = test_case["answerable"]

    # Retrieve the top K chunks for the question.
    results = retriever.retrieve(question, top_k=TOP_K)
    retrieved_ids = [str(result.id) for result in results]

    # Count retrieved chunks that have been labeled relevant.
    relevant_ranks = [
        rank
        for rank, point_id in enumerate(retrieved_ids, start=1)
        if point_id in relevant_ids
    ]

    hits = len(relevant_ranks)
    hit_rate = 1.0 if hits > 0 else 0.0

    # Recall is undefined when no relevant chunks are labeled.
    if relevant_ids:
        recall = hits / len(relevant_ids)
        precision = hits / TOP_K
        reciprocal_rank = (
            1 / relevant_ranks[0] if relevant_ranks else 0.0
        )
    else:
        recall = None
        precision = None
        reciprocal_rank = None

    return {
        "question": question,
        "answerable": answerable,
        "relevant_count": len(relevant_ids),
        "retrieved_relevant_count": hits,
        "recall_at_5": recall,
        "precision_at_5": precision,
        "hit_rate_at_5": hit_rate,
        "mrr": reciprocal_rank,
        "retrieved_point_ids": "|".join(retrieved_ids),
    }


def main():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    retriever = Retriever()
    rows = [
        evaluate_question(retriever, test_case)
        for test_case in dataset
    ]

    # Save per-question results.
    fieldnames = list(rows[0].keys()) if rows else []

    with RESULTS_PATH.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Aggregate retrieval metrics for answerable questions only.
    answerable_rows = [
        row for row in rows if row["relevant_count"] > 0
    ]

    print("\nRETRIEVAL EVALUATION RESULTS")
    print("-" * 40)

    for row in rows:
        print(f"\nQuestion: {row['question']}")
        print(f"Recall@5: {row['recall_at_5']}")
        print(f"Precision@5: {row['precision_at_5']}")
        print(f"Hit Rate@5: {row['hit_rate_at_5']}")
        print(f"MRR: {row['mrr']}")

    if answerable_rows:
        print("\nOVERALL METRICS")
        print("-" * 40)

        metric_names = [
            "recall_at_5",
            "precision_at_5",
            "hit_rate_at_5",
            "mrr",
        ]

        for metric in metric_names:
            average = sum(
                row[metric] for row in answerable_rows
            ) / len(answerable_rows)

            print(f"{metric}: {average:.4f} ({average:.2%})")

    print(f"\nResults saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
