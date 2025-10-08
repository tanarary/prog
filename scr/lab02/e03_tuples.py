def format_record(rec: tuple[str, str, float]) -> str:
    if len(rec) == 3:
        fio = rec[0].split()
        if len(fio) == 2:
            fio1 = fio[0] + ' ' + fio[0][0].capitalize() + '.'
        if len(fio) == 3:
            fio1 = fio[0].capitalize() + ' ' + fio[1][0].capitalize() + '.' + fio[2][0].capitalize() + '.'
        if len(fio) < 2:
            raise ValueError
        gr = rec[1]
        gpa = float(rec[2])
        return fio1 + ', гр. ' + gr + ', GPA ' + f"{gpa: .2f}"
    if len(rec) != 3:
        raise ValueError
    if type(rec[0]) != str or type(rec[1]) != str or type(rec[2]) != float:
        raise TypeError
    

print(format_record(("Иванов Иван Иванович","BIVT-25",4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))

    


    