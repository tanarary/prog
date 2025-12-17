import json
from typing import List
from models import Student
def students_to_json(students: List[Student], path: str) -> None:
    data = [student.to_dict() for student in students]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Данные сохранены в {path}")
def students_from_json(path: str) -> List[Student]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        students = []
        for item in data:
            try:
                student = Student.from_dict(item)
                students.append(student)
            except ValueError as e:
                print(f"Не удалось создать студента из записи {item}: {e}")
        print(f"Загружено {len(students)} студентов из {path}")
        return students   
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON файла: {e}")
        return []
if __name__ == "__main__": 
    students = [
        Student("Иванов Иван Иванович", "2007-02-19", "БИВТ-1-1", 3.5),
        Student("Петров Петр Петрович", "2006-01-01", "БИ-2-1", 4.5),
        Student("Семёнов Семён Семёнович", "2005-03-03", "ПМ-3-1", 3.9)
    ]
    students_to_json(students, "scr/lab08/students_output.json")
    loaded_students = students_from_json("scr/lab08/students_input.json")
    for student in loaded_students:
        print(student)