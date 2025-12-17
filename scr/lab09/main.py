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


