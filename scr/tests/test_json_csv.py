import pytest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scr.lab05.e01_json_to_csv import json_to_csv, csv_to_json


def test_json_to_csv_basic(tmp_path):
    src = tmp_path / "test.json"
    dst = tmp_path / "test.csv"
    test_data = [{"name": "Анна", "age": 25}]
    src.write_text(json.dumps(test_data), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    assert dst.exists()


def test_json_to_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        json_to_csv("nonexistent.json", "output.csv")


def test_csv_to_json_basic(tmp_path):
    src = tmp_path / "test.csv"
    dst = tmp_path / "test.json"
    src.write_text("name,age\nAlice,25", encoding="utf-8")
    csv_to_json(str(src), str(dst))
    assert dst.exists()


def test_csv_to_json_file_not_found():
    with pytest.raises(FileNotFoundError):
        csv_to_json("nonexistent.csv", "output.json")


def test_json_to_csv_invalid_json(tmp_path):
    src = tmp_path / "invalid.json"
    dst = tmp_path / "output.csv"
    src.write_text("{ invalid json }", encoding="utf-8")
    with pytest.raises(ValueError, match="Некорректный JSON"):
        json_to_csv(str(src), str(dst))


def test_json_to_csv_empty_json(tmp_path):
    src = tmp_path / "empty.json"
    dst = tmp_path / "output.csv"
    src.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON файл пуст"):
        json_to_csv(str(src), str(dst))


def test_json_to_csv_not_array(tmp_path):
    src = tmp_path / "not_array.json"
    dst = tmp_path / "output.csv"
    src.write_text('{"a": 1}', encoding="utf-8")
    with pytest.raises(ValueError, match="JSON должен содержать массив объектов"):
        json_to_csv(str(src), str(dst))


def test_csv_to_json_empty_file(tmp_path):
    src = tmp_path / "empty.csv"
    dst = tmp_path / "output.json"
    src.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="CSV файл пуст"):
        csv_to_json(str(src), str(dst))


def test_csv_to_json_csv_error_coverage(tmp_path):
    """Тест для покрытия обработки csv.Error."""
    src = tmp_path / "csv_error.csv"
    dst = tmp_path / "output.json"

    very_long_field = "x" * 1000000
    csv_content = f'name,data\n"Test","{very_long_field}"'

    src.write_text(csv_content, encoding="utf-8")

    try:
        csv_to_json(str(src), str(dst))
        assert dst.exists()
    except ValueError as e:
        assert "Некорректный CSV" in str(e)