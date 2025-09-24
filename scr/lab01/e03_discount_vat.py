price = float(input('Введите цену: '))
sale = float(input('Введите скидку: '))
vat =  float(input('Введите НДС: '))
base = price * (1 - sale/100)
print(f"""База после скидки: {base} ₽
НДС:               {base * (vat/100)} ₽
Итого к оплате:    {base * (vat/100) + base} ₽""")