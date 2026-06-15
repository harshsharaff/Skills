#!/usr/bin/env python3
"""Summarize a CSV file into per-column statistics.

Usage:
    python scripts/summarize.py data.csv
Prints a JSON summary to stdout.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def _as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def summarize_rows(rows: list[dict[str, str]]) -> dict:
    columns: dict[str, dict] = {}
    fieldnames = list(rows[0].keys()) if rows else []

    for col in fieldnames:
        values = [r.get(col, "") for r in rows]
        non_null = [v for v in values if v not in ("", None)]
        nums = [n for v in non_null if (n := _as_float(v)) is not None]

        stat: dict = {
            "count": len(non_null),
            "nulls": len(values) - len(non_null),
        }
        if non_null and len(nums) == len(non_null):
            stat["type"] = "number"
            stat["min"] = min(nums)
            stat["max"] = max(nums)
            stat["mean"] = round(sum(nums) / len(nums), 6)
        else:
            stat["type"] = "string"
        columns[col] = stat

    return {"rows": len(rows), "columns": columns}


def summarize_csv(path: str | Path) -> dict:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return summarize_rows(rows)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: summarize.py <file.csv>", file=sys.stderr)
        return 2
    print(json.dumps(summarize_csv(argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
