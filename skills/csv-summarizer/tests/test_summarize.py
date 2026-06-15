import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.summarize import summarize_csv, summarize_rows


def test_summarize_rows_numeric_and_string():
    rows = [
        {"name": "a", "age": "30"},
        {"name": "b", "age": "40"},
        {"name": "c", "age": ""},
    ]
    out = summarize_rows(rows)
    assert out["rows"] == 3

    age = out["columns"]["age"]
    assert age["type"] == "number"
    assert age["count"] == 2
    assert age["nulls"] == 1
    assert age["min"] == 30.0
    assert age["max"] == 40.0
    assert age["mean"] == 35.0

    name = out["columns"]["name"]
    assert name["type"] == "string"
    assert name["nulls"] == 0


def test_summarize_csv_reads_file(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("x,y\n1,foo\n2,bar\n", encoding="utf-8")
    out = summarize_csv(p)
    assert out["rows"] == 2
    assert out["columns"]["x"]["type"] == "number"
    assert out["columns"]["y"]["type"] == "string"
