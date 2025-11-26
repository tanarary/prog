# tests/test_text.py
import pytest
from lib.text import normalize, tokenize, count_freq, top_n

@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\\nМИр\\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\\r\\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),
        ("!!!", "!!!"),
        ("повтор повтор Повтор", "повтор повтор повтор"),
    ],
)
def test_normalize(source, expected):
    assert normalize(source) == expected

@pytest.mark.parametrize(
    "source, expected",
    [
        ("hello world", ["hello", "world"]),
        ("привет, мир!", ["привет", "мир"]),
        ("", []),
        ("word word word", ["word", "word", "word"]),
        ("спецсимволы! @#", ["спецсимволы"]),
    ],
)
def test_tokenize(source, expected):
    assert tokenize(source) == expected

@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["a", "b", "a", "c", "b", "b"], {"a": 2, "b": 3, "c": 1}),
        ([], {}),
        (["x", "x", "x"], {"x": 3}),
    ],
)
def test_count_freq(tokens, expected):
    assert count_freq(tokens) == expected

def test_top_n_tie_breaker():
    freq = {"apple": 2, "banana": 2, "cherry": 1}
    expected = [("apple", 2), ("banana", 2), ("cherry", 1)]
    assert top_n(freq, 10) == expected

@pytest.mark.parametrize(
    "freq, n, expected",
    [
        ({"a": 3, "b": 2, "c": 1}, 2, [("a", 3), ("b", 2)]),
        ({"a": 1, "b": 1, "c": 1}, 3, [("a", 1), ("b", 1), ("c", 1)]),
    ],
)
def test_top_n(freq, n, expected):
    assert top_n(freq, n) == expected

# tests/test_json_csv.py
import pytest
import json
import csv
from pathlib import Path
from lib.text import json_to_csv, csv_to_json

def test_json_to_csv_roundtrip(tmp_path: Path):
    src = tmp_path / "data.json"
    dst = tmp_path / "data.csv"
    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    json_to_csv(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert {"name", "age"} <= set(rows[0].keys())

def test_csv_to_json_roundtrip(tmp_path: Path):
    src = tmp_path / "data.csv"
    dst = tmp_path / "data_out.json"
    csv_content = "name,age\nAlice,22\nBob,25\n"
    src.write_text(csv_content, encoding="utf-8")
    csv_to_json(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert all("name" in item and "age" in item for item in data)

@pytest.mark.parametrize(
    "func, src_name, dst_name",
    [
        (json_to_csv, "empty.json", "out.csv"),
        (csv_to_json, "empty.csv", "out.json"),
    ],
)
def test_value_error_on_empty_file(tmp_path: Path, func, src_name, dst_name):
    src = tmp_path / src_name
    dst = tmp_path / dst_name
    src.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        func(str(src), str(dst))

@pytest.mark.parametrize(
    "func, src_name, dst_name",
    [
        (json_to_csv, "nofile.json", "out.csv"),
        (csv_to_json, "nofile.csv", "out.json"),
    ],
)
def test_file_not_found_error(tmp_path: Path, func, src_name, dst_name):
    src = tmp_path / src_name
    dst = tmp_path / dst_name
    # No file created
    with pytest.raises(FileNotFoundError):
        func(str(src), str(dst))
