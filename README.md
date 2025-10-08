lab# prog
## Лабораторная работа 1

### Задание 1
```python
name = input('Имя: ')
age = int(input('Возраст: '))
print(f"Привет, {name}! Через год тебе будет {age + 1}.")
```
![Картинка 1](/scr/lab01/img/e01_img.png)

### Задание 2
```python
a = float(input('a: ').replace(',','.'))
b = float(input('b: ').replace(',','.'))
print(f"sum={round(a+b,2)}; avg={round((a+b)/2,2)}")
```
![Картинка 2](/scr/lab01/img/e02_img.png)

### Задание 3
```python
price = float(input('Введите цену: '))
sale = float(input('Введите скидку: '))
vat =  float(input('Введите НДС: '))
base = price * (1 - sale/100)
print(f"""База после скидки: {base} ₽
НДС:               {base * (vat/100)} ₽
Итого к оплате:    {base * (vat/100) + base} ₽""")
```
![Картинка 3](/scr/lab01/img/e03_img.png)

### Задание 4
```python
m = int(input('Минуты: '))
print(f"{m // 60}:{m% 60}")
```
![Картинка 4](/scr/lab01/img/e04_img.png)

### Задание 5
```python
name = input('Имя: ')
ln = [nam[0] for nam in name.split()]
print('Инициалы:', ''.join(ln))
print('Длина (символов):', len(' '.join(name.split())))
```
![Картинка 5](/scr/lab01/img/e05_img.png)

## Лабораторная работа 2

### Задание 1
```python
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    return min(nums), max(nums)
```
![Картинка 1](/scr/lab02/img/e01_1_img.png)

### Задание 2
```python
def unique_sorted(ls: list[float | int]) -> list[float | int]:
    return sorted(set(ls))

```
    
![Картинка 2](/scr/lab02/img/e01_2_img.png)


### Задание 3
```python
def flatten(mat: list[list | tuple]) -> list:
    fl = []
    for i in mat:
        if type(i) == list or type(i) == tuple:
            fl.extend(i)
        else:
            raise TypeError
    return fl

```
![Картинка 3](/scr/lab02/img/e01_3_img.png)

### Задание 4
```python
def transpose(mat: list[list[float | int]]) -> list[list]:
    for i in range(len(mat)-1):
        if len(mat[i]) == len(mat[i+1]):
            continue
        else:
            raise ValueError
    new = []
    if mat == []:
        new = []
    else:
        for i in range(len(mat[0])):
            new_row = []
            for row in mat:
                new_row.append(row[i])
            new.append(new_row)
    return new


```
![Картинка 4](/scr/lab02/img/e02_1_img.png)


### Задание 5
```python
def row_sums(mat: list[list[float | int]]) -> list[float]:
    for i in range(len(mat)-1):
        if len(mat[i]) == len(mat[i+1]):
            continue
        else:
            raise ValueError
    new = [] 
    for row in mat:
        s = 0
        for i in row:
            if type(i) == float or type(i) == int:
                s += i
            else:
                raise TypeError
        new.append(s)
    return new 
```
![Картинка 5](/scr/lab02/img/e02_2_img.png)

### Задание 6
```python
def col_sums(mat: list[list[float | int]]) -> list[float]:
    for i in range(len(mat)-1):
        if len(mat[i]) == len(mat[i+1]):
            continue
        else:
            raise ValueError
    new = [] 
    for i in range(len(mat[0])):
        s = 0
        for row in mat:
            s += row[i]
        new.append(s)
    return new 
```
![Картинка 5](/scr/lab02/img/e02_3_img.png)

### Задание 7
```python
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
```
![Картинка 7](/scr/lab02/img/e03_img.png)