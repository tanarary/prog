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
print(f"""База после скидки: {sale} ₽
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