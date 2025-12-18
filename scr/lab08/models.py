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
