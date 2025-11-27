import pytest
import json
import csv
from pathlib import Path
import sys
import os


# Добавляем корень проекта, где лежит папка src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scr.lab05.e01_json_to_csv import json_to_csv, csv_to_json


# Успешные тесты JSON -> CSV
@pytest.mark.parametrize(
    "data,expected",
    [
        ([{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}], 2),
        ([{"name": "Alice", "active": True, "score": 95.5}], 1),
        ([{"name": "Alice", "comment": ""}], 1),
        ([{"name": "Алиса", "message": "Привет!"}], 1),
        ([{"name": "Alice", "age": None}], 1),
        ([{"id": 1, "value": "test"}], 1),
        ([{"a": 1}, {"a": 2}, {"a": 3}], 3),
        ([{"x": "test1"}, {"x": "test2"}], 2),
    ],
)
def test_json_to_csv_success(tmp_path, data, expected):
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"
    src.write_text(json.dumps(data), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == expected


# Успешные тесты CSV -> JSON
@pytest.mark.parametrize(
    "content,expected",
    [
        ("name,age\nAlice,25\nBob,30", 2),
        ('name,desc\n"Alice","Test"', 1),
        ("name;age\nAlice;25\nBob;30", 2),
        ('name,age\n"Alice","25"\n"Bob","30"', 2),
        ("name,age,city\nAlice,25,\nBob,30,London", 2),
        ("name\nAlice\nBob", 2),
        ("id,name,age\n1,Alice,25\n2,Bob,30", 2),
        ("first,last\nJohn,Doe\nJane,Smith", 2),
        ("a,b,c\n1,2,3\n4,5,6", 2),
        ("col1\nval1\nval2", 2),
    ],
)
def test_csv_to_json_success(tmp_path, content, expected):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text(content, encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == expected


# Тесты ошибок JSON
@pytest.mark.parametrize(
    "content,error",
    [
        (None, FileNotFoundError),
        ("{ invalid json }", ValueError),
        ("", ValueError),
        ('{"name": "test"}', ValueError),
        ("[]", ValueError),
        (b"\xff\xfe", ValueError),
        ('[{"name": "test"},]', ValueError),
        ('[{"name": "test}]', ValueError),
    ],
)
def test_json_to_csv_errors(tmp_path, content, error):
    dst = tmp_path / "output.csv"
    if content is None:
        with pytest.raises(error):
            json_to_csv("nonexistent.json", str(dst))
    else:
        src = tmp_path / "test.json"
        if isinstance(content, bytes):
            src.write_bytes(content)
        else:
            src.write_text(content, encoding="utf-8")
        with pytest.raises(error):
            json_to_csv(str(src), str(dst))


# Тесты ошибок CSV
@pytest.mark.parametrize(
    "content,error",
    [
        (None, FileNotFoundError),
        ("", ValueError),
        (b"\xff\xfe", ValueError),
    ],
)
def test_csv_to_json_errors(tmp_path, content, error):
    dst = tmp_path / "output.json"
    if content is None:
        with pytest.raises(error):
            csv_to_json("nonexistent.csv", str(dst))
    else:
        src = tmp_path / "test.csv"
        if isinstance(content, bytes):
            src.write_bytes(content)
        else:
            src.write_text(content, encoding="utf-8")
        with pytest.raises(error):
            csv_to_json(str(src), str(dst))


# Специальные тесты
def test_json_csv_roundtrip(tmp_path):
    original = tmp_path / "original.json"
    csv_file = tmp_path / "intermediate.csv"
    final = tmp_path / "final.json"
    data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
    original.write_text(json.dumps(data), encoding="utf-8")
    json_to_csv(str(original), str(csv_file))
    csv_to_json(str(csv_file), str(final))
    with final.open(encoding="utf-8") as f:
        result = json.load(f)
    assert len(result) == 2
    assert result[0]["name"] == "Alice"


def test_csv_only_header(tmp_path):
    src = tmp_path / "header.csv"
    dst = tmp_path / "output.json"
    src.write_text("name,age", encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 0


def test_wrong_extension_json(tmp_path):
    src = tmp_path / "test.txt"
    dst = tmp_path / "test.csv"
    src.write_text('[{"name": "test"}]', encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_wrong_extension_csv(tmp_path):
    src = tmp_path / "test.txt"
    dst = tmp_path / "test.json"
    src.write_text("name,age\nAlice,25", encoding="utf-8")
    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


# Дополнительные тесты
def test_large_dataset(tmp_path):
    src = tmp_path / "large.json"
    dst = tmp_path / "large.csv"
    data = [{"id": i} for i in range(10)]
    src.write_text(json.dumps(data), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 10


def test_special_chars_json(tmp_path):
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"
    data = [{"text": "Hello", "quotes": 'Text "quotes"'}]
    src.write_text(json.dumps(data), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    assert dst.exists()


def test_empty_values_csv(tmp_path):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text("name,age,city\nAlice,25,\nBob,,London", encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 2


def test_boolean_values(tmp_path):
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"
    data = [{"flag": True, "active": False}]
    src.write_text(json.dumps(data), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["flag"] == "True"


def test_single_row_csv(tmp_path):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text("name,age\nAlice,25", encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1


def test_comma_in_quotes(tmp_path):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text('name,address\n"Alice","Street 1, Apt 2"', encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert data[0]["address"] == "Street 1, Apt 2"


def test_content_validation_json_to_csv(tmp_path):
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"
    data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
    src.write_text(json.dumps(data), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert set(rows[0].keys()) == {"name", "age"}
    assert rows[0]["name"] == "Alice"


def test_content_validation_csv_to_json(tmp_path):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text("name,age,score\nAlice,25,95.5\nBob,30,88.0", encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert data[0]["name"] == "Alice"
    assert data[0]["age"] == "25"


def test_unicode_content(tmp_path):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text("text\nПривет", encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1


def test_multiple_roundtrips(tmp_path):
    for i in range(3):
        json_file = tmp_path / f"test{i}.json"
        csv_file = tmp_path / f"test{i}.csv"
        final_json = tmp_path / f"final{i}.json"
        data = [{"id": i, "value": f"test{i}"}]
        json_file.write_text(json.dumps(data), encoding="utf-8")
        json_to_csv(str(json_file), str(csv_file))
        csv_to_json(str(csv_file), str(final_json))
        with final_json.open(encoding="utf-8") as f:
            result = json.load(f)
        assert len(result) == 1


def test_numeric_data(tmp_path):
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"
    data = [{"number": 123, "float": 45.67}]
    src.write_text(json.dumps(data), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["number"] == "123"


def test_mixed_data_types(tmp_path):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text("string,number,boolean\nhello,123,true", encoding="utf-8")
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        data = json.load(f)
    assert data[0]["string"] == "hello"
    assert data[0]["number"] == "123"
