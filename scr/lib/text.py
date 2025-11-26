import re
import json
import csv
import csv
from pathlib import Path
from openpyxl import Workbook
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    result = text
    
    if casefold:
        result = result.casefold()    
    if yo2e:
        result = result.replace('ё', 'е').replace('Ё', 'е')
    
    for char in ['\t', '\r', '\n']:
        result = result.replace(char, ' ')
    
    result = re.sub(r'\s+', ' ', result).strip()
    return result

def tokenize(text: str) -> List[str]:
    pattern = r'\w+(?:-\w+)*'
    tokens = re.findall(pattern, text)
    return tokens

def count_freq(tokens: List[str]) -> Dict[str, int]:
    return Counter(tokens)

def top_n(freq: Dict[str, int], n: int = 5) -> List[Tuple[str, int]]:
    items = list(freq.items())
    sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
    return sorted_items[:n]

if __name__ == "__main__":
    test_text = "Привет, мир! Привет!!! Тест-тест проверка."
    print("Исходный текст:", test_text)
    
    norm_text = normalize(test_text)
    print("Нормализованный:", norm_text)
    
    tokens = tokenize(norm_text)
    print("Токены:", tokens)
    
    freq = count_freq(tokens)
    print("Частоты:", freq)
    
    top_3 = top_n(freq, 3)
    print("Топ-3:", top_3)

def json_to_csv(json_path: str, csv_path: str) -> None:

    json_file = Path(json_path)
    csv_file = Path(csv_path)
    ensure_relative(json_file)
    ensure_relative(csv_file)
    
    if not json_file.exists():
        raise FileNotFoundError(f"Файл {json_path} не найден")
    
    if json_file.suffix.lower() != '.json':
        raise ValueError("Неверный тип файла. Ожидается .json")
    
    try:
        with json_file.open('r', encoding='utf-8') as f:
            data = json.load(f) #преобразовывет в питоновский файл   
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения JSON: {e}")
    
    if not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список объектов")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON должны быть словарями")
    
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())

    if data:
        first_item_keys = list(data[0].keys())
        remaining_keys = sorted(all_keys - set(first_item_keys))
        fieldnames = first_item_keys + remaining_keys
    else:
        fieldnames = sorted(all_keys)
    # Запись в CSV
    try:
        with csv_file.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                complete_row = {key: row.get(key, '') for key in fieldnames}
                writer.writerow(complete_row)
    except Exception as e:
        raise ValueError(f"Ошибка записи CSV: {e}")

def csv_to_json(csv_path: str, json_path: str) -> None:
  
    csv_file = Path(csv_path)
    json_file = Path(json_path)
    
    if not csv_file.exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден")

    if csv_file.suffix.lower() != '.csv':
        raise ValueError("Неверный тип файла. Ожидается .csv")
    
    try:
        with csv_file.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError("CSV файл не содержит заголовка")
            
            data = list(reader)
            
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")

    if not data:
        raise ValueError("Пустой CSV файл")

    try:
        with json_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2) #из питона в json
    except Exception as e:
        raise ValueError(f"Ошибка записи JSON: {e}")
    
def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    Использует openpyxl.
    Первая строка CSV — заголовок.
    Лист называется "Sheet1".
    Колонки — автоширина по длине текста (не менее 8 символов).
    """
    csv_file = Path(csv_path)
    xlsx_file = Path(xlsx_path)

    if not csv_file.is_file():
        raise FileNotFoundError(f"File {csv_path} not found")

    with csv_file.open(encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    if len(data) == 0:
        raise ValueError("CSV file is empty")

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    for row in data:
        ws.append(row)

    # Установить автоширину колонок (не менее 8 символов)
    for col_idx, col_cells in enumerate(ws.columns, start=1):
        max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
        adjusted_width = max(max_length, 8)
        col_letter = ws.cell(row=1, column=col_idx).column_letter
        ws.column_dimensions[col_letter].width = adjusted_width

    wb.save(xlsx_file)
    