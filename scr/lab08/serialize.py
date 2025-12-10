import json
from pathlib import Path
from typing import List
import sys
import os

# Добавляем путь к scr/lab08
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import Student

def students_to_json(students: List[Student], path: str | Path) -> None:
    """Сохраняет список студентов в JSON файл."""
    data = [s.to_dict() for s in students]
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    with path_obj.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def students_from_json(path: str | Path) -> List[Student]:
    """Читает JSON файл и возвращает список студентов."""
    path_obj = Path(path)
    if not path_obj.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    with path_obj.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать массив студентов")
    
    students = []
    for item in data:
        student = Student.from_dict(item)
        students.append(student)
    
    return students
