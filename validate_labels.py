#!/usr/bin/env python3
"""Summarize and validate the project's labels.csv."""

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

VALID_LABELS = ("analysis", "announcement", "hot_take", "reaction")
DEFAULT_CSV = Path(__file__).resolve().parent / "labels.csv"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=DEFAULT_CSV,
        help=f"CSV file to validate (default: {DEFAULT_CSV})",
    )
    args = parser.parse_args()

    with args.csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        missing_columns = {"text", "label"} - set(reader.fieldnames or ())
        if missing_columns:
            parser.error(
                f"{args.csv_path} is missing required column(s): "
                f"{', '.join(sorted(missing_columns))}"
            )

        label_counts = Counter()
        label_records = defaultdict(list)
        text_records = defaultdict(list)
        total_rows = 0

        for record_number, row in enumerate(reader, start=1):
            total_rows += 1
            label = row["label"] or ""
            text = row["text"] or ""
            label_counts[label] += 1
            label_records[label].append(record_number)
            text_records[text].append(record_number)

    print(f"Total rows: {total_rows}")
    print("Label counts and percentages:")
    labels = list(VALID_LABELS)
    labels.extend(sorted(label for label in label_counts if label not in VALID_LABELS))
    for label in labels:
        count = label_counts[label]
        percentage = count / total_rows * 100 if total_rows else 0
        display_label = repr(label) if label not in VALID_LABELS else label
        print(f"  {display_label}: {count} ({percentage:.1f}%)")

    invalid_labels = [
        label for label in label_counts if label not in VALID_LABELS
    ]
    print(f"Invalid label strings: {len(invalid_labels)}")
    for label in sorted(invalid_labels):
        records = ", ".join(str(number) for number in label_records[label])
        print(
            f"  {label!r}: {label_counts[label]} occurrence(s) "
            f"(CSV records: {records})"
        )

    duplicates = [
        (text, records)
        for text, records in text_records.items()
        if len(records) > 1
    ]
    print(f"Duplicate texts: {len(duplicates)}")
    for text, records in sorted(duplicates, key=lambda item: item[1][0]):
        record_list = ", ".join(str(number) for number in records)
        print(f"  CSV records {record_list}: {text!r}")


if __name__ == "__main__":
    main()
