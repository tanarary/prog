from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, Any
import json
from pathlib import Path

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        """Валидация формата даты YYYY-MM-DD и диапазона GPA 0..5"""
        # Проверка формата даты
        try:
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"birthdate '{self.birthdate}' must be in YYYY-MM-DD format")
        
        # Проверка GPA
        if not (0 <= self.gpa <= 5):
            raise ValueError(f"gpa {self.gpa} must be between 0 and 5")

    def age(self) -> int:
        """Возвращает количество полных лет студента."""
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth_date.year
        # Корректировка если день рождения еще не наступил
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация объекта Student в словарь."""
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Student':
        """Десериализация словаря в объект Student."""
        required = {"fio", "birthdate", "group", "gpa"}
        if not required.issubset(d):
            missing = required - set(d.keys())
            raise ValueError(f"Missing required fields: {missing}")
        return cls(
            fio=str(d["fio"]),
            birthdate=str(d["birthdate"]),
            group=str(d["group"]),
            gpa=float(d["gpa"])
        )

    def __str__(self) -> str:
        """Красивый строковый вывод."""
        return f"{self.fio}, группа {self.group}, GPA {self.gpa:.2f}, {self.age()} лет"
