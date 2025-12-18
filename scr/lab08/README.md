## Лабораторная работа 8

### Задание А (models.py)
```python
from dataclasses import dataclass
from datetime import datetime, date
import re

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float
    
    def __post_init__(self):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', self.birthdate):
            raise ValueError(f"Неверный формат даты: {self.birthdate}. Используйте формат YYYY-MM-DD")
        try:
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Неверная дата: {self.birthdate}")
        if not (0 <= self.gpa <= 5):
            raise ValueError(f"Средний балл должен быть в диапазоне от 0 до 5, получено: {self.gpa}")
        if len(self.fio.split()) < 2:
            raise ValueError(f"ФИО должно содержать имя и фамилию: {self.fio}")
    
    def age(self) -> int:
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        today = date.today()
        
        age = today.year - birth_date.year
        
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    
    def to_dict(self) -> dict:
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            fio=data.get("fio", ""),
            birthdate=data.get("birthdate", ""),
            group=data.get("group", ""),
            gpa=data.get("gpa", 0.0)
        )
    
    def __str__(self) -> str:
        return f"{self.fio}, группа: {self.group}, возраст: {self.age()}, средний балл: {self.gpa}"


if __name__ == "__main__":
    try:
        student = Student(
            fio="Иванов Иван Иванович",
            birthdate="2007-12-14",
            group="БИВТ-25-1",
            gpa=3.3
        )
        print(student)
        print(f"Словарь: {student.to_dict()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

```
![models](/scr/lab08/img/models_img.png)


### Задание B (serialize.py)

```python
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

```

### Файл src/lab08/students_input.json
```python
[
  {
    "fio": "Иванов Иван Иванович",
    "birthdate": "2007-02-19",
    "group": "БИВТ-1-1",
    "gpa": 3.5
  },
  {
    "fio": "Петров Петр Петрович",
    "birthdate": "2006-01-01",
    "group": "БИ-2-1",
    "gpa": 4.5
  },
  {
    "fio": "Семёнов Семён Семёнович",
    "birthdate": "2005-03-03",
    "group": "ПМ-3-1",
    "gpa": 2.9
  }
]
```
## Вывод в терминале 
![vv](/scr/lab08/img/serialize_img.png)

## После выполнения программы, был создан файл students_output.json
![stud_output](/scr/lab08/img/output_img.png)

