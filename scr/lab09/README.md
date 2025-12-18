## Лабораторная работа 9

### A.Реализация класса Group
```python
import os
import sys
import csv
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scr.lab08.models import Student

class Group:
    HEADER = ["fio", "birthdate", "group", "gpa"]

    def __init__(self, storage_path):
        self.path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        if not self.path.exists():
            with self.path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADER)

    def _read_all(self):
        students = []
        with self.path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(
                    Student(
                        fio=row["fio"],
                        birthdate=row["birthdate"],
                        group=row["group"],
                        gpa=float(row["gpa"]),
                    )
                )
        return students

    def list(self):
        return self._read_all()

    def add(self, student):
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [student.fio, student.birthdate, student.group, student.gpa]
            )

    def find(self, substr):
        substr = substr.lower()
        return [s for s in self._read_all() if substr in s.fio.lower()]

    def remove(self, fio):
        students = self._read_all()
        students = [s for s in students if s.fio != fio]

        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            for s in students:
                writer.writerow([s.fio, s.birthdate, s.group, s.gpa])

    def update(self, fio: str, **fields):
        students = self._read_all()

        for student in students:
            if student.fio == fio:
                for key, value in fields.items():
                    setattr(student, key, value)
                break

        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            for st in students:
                writer.writerow([st.fio, st.birthdate, st.group, st.gpa])


```



### Код для проверки main.py

```python
from group import Group
from scr.lab08.models import Student

def print_students(title, students):
    print("\n" + title)
    for s in students:
        print(f"{s.fio} | {s.birthdate} | {s.group} | {s.gpa}")

g = Group("scr/lab09/students.csv")

print_students("Изначальный CSV:", g.list())

new_st = Student("Морозов Михаил Андреевич", "2007-12-21", "БИВТ-25-8", 2.2)
g.add(new_st)
print_students("После добавления:", g.list())

found = g.find("те")
print_students("Поиск 'те':", found)

g.update("Иванов Иван Иванович", gpa=4.1, group="БИВТ-25-6")
print_students("После обновления данных Иванова:", g.list())

g.remove("Соколов Артём Юрьевич")
print_students("После удаления Гадаловой:", g.list())


```

### Входной файл CSV:

![vvcsv](/scr/lab09/img/do.png)

### Запуск тестов

![tests](/scr/lab09/img/group_img.png)

### Файл CSV после тестов:
![vvcsv2](/scr/lab09/img/posle.png)