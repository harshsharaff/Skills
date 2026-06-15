---
name: csv-summarizer
description: >-
  Summarize CSV files into per-column stats (type, count, nulls, min/max/mean for
  numbers). Use when the user wants a quick overview of a CSV or tabular dataset.
disable-model-invocation: true
---
# CSV Summarizer

## Instructions

Run the helper script to produce a JSON summary; do not hand-compute stats.

```bash
python scripts/summarize.py path/to/data.csv
```

Output is JSON: `{ "rows": N, "columns": { name: {type, count, nulls, ...} } }`.
Numeric columns include `min`, `max`, `mean`. Present the result as a short table
and call out anything notable (high null counts, suspicious ranges).

## Utility scripts

**summarize.py** — read a CSV and print a JSON summary.
```bash
python scripts/summarize.py data.csv > summary.json
```

## Requirements

Standard library only (see [requirements.txt](requirements.txt)).
