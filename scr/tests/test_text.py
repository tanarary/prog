import pytest
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scr.lib.text import normalize, tokenize, count_freq, top_n


def test_normalize_simple():
    result = normalize("ПРИВЕТ")
    assert result == "привет"


def test_normalize_empty():
    result = normalize("")
    assert result == ""


def test_tokenize_basic():
    result = tokenize("привет мир")
    assert result == ["привет", "мир"]


def test_count_freq_basic():
    result = count_freq(["яблоко", "банан", "яблоко"])
    assert result == {"яблоко": 2, "банан": 1}


def test_top_n_basic():
    freq = {"яблоко": 5, "банан": 3, "апельсин": 7}
    result = top_n(freq, 2)
    assert result == [("апельсин", 7), ("яблоко", 5)]


def test_count_freq_empty():
    assert count_freq([]) == {}


def test_top_n_edge_cases():
    assert top_n({}, 5) == []
    assert top_n({"a": 1}, 0) == []
    assert top_n({"a": 1}, -1) == []


def test_tokenize_numbers():
    assert "123" in tokenize("test 123")


def test_count_freq_completely_empty():
    result = count_freq([])
    assert result == {}
    assert len(result) == 0


def test_count_freq_absolutely_empty():
    assert count_freq([]) == {}


def test_tokenize_empty_string():
    result = tokenize("")
    assert result == []