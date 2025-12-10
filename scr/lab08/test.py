import json
import sys
import os
from pathlib import Path

# Фикс импортов - добавляем scr/lab08 в sys.path
lab08_dir = Path(__file__).parent
sys.path.insert(0, str(lab08_dir))

from models import Student
from serialize import students_to_json, students_from_json

# Корень проекта и данные
BASE_DIR = lab08_dir.parent.parent  # scr/lab08/ -> scr/ -> prog/
DATA_DIR = BASE_DIR / "data" / "lab08"
DATA_DIR.mkdir(parents=True, exist_ok=True)

input_file = DATA_DIR / "students_input.json"
output_file = DATA_DIR / "students_output.json"

print(f"Рабочая папка: {Path.cwd()}")
print(f"Данные: {DATA_DIR}")

# Создаем тестовые данные если нет
if not input_file.exists():
    print("Создаем students_input.json...")
    sample_data = [
        {"fio": "Иванов Иван Иванович", "birthdate": "2004-05-12", "group": "SE-01", "gpa": 4.5},
        {"fio": "Петров Петр Петрович", "birthdate": "2003-11-25", "group": "SE-01", "gpa": 3.8},
        {"fio": "Сидорова Анна Сергеевна", "birthdate": "2005-02-18", "group": "SE-02", "gpa": 4.9}
    ]
    with input_file.open("w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

print("\n=== 1. Создание студентов ===")
with input_file.open(encoding="utf-8") as f:
    students_data = json.load(f)
students = [Student.from_dict(d) for d in students_data]

for i, student in enumerate(students, 1):
    print(f"{i}. {student}")

print("\n=== 2. Сериализация ===")
students_to_json(students, output_file)
print(f"✓ {output_file} создан")

print("\n=== 3. Десериализация ===")
loaded = students_from_json(output_file)
for i, student in enumerate(loaded, 1):
    print(f"{i}. {student}")


assert len(students) == len(loaded), "Количество не совпадает"

