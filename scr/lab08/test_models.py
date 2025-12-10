import json
from models import Student
from pathlib import Path

# Путь к данным (относительно scr/lab08/)
input_file = Path("scr/data/lab8/students_input.json")

print("=== Загрузка студентов ===")
with input_file.open(encoding="utf-8") as f:
    students_data = json.load(f)

students = [Student.from_dict(d) for d in students_data]

print("=== Тестирование методов ===")
for i, student in enumerate(students, 1):
    print(f"\nСтудент {i}:")
    print(f"  {student}")
    print(f"  Возраст: {student.age()} лет")
    print(f"  Словарь: {student.to_dict()}")

print("\n=== Сериализация в JSON ===")
output_data = [s.to_dict() for s in students]
output_file = Path("scr/data/lab8/students_output.json")
with output_file.open("w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)
print("students_output.json создан!")





