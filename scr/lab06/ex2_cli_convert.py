import argparse
from pathlib import Path
import sys
import os


# Добавляем корень проекта, где лежит папка src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scr.lab05.e01_json_to_csv import json_to_csv, csv_to_json
from scr.lab05.e02_csv_to_xlxs import csv_to_xlsx


def main():
    parser = argparse.ArgumentParser(description="Конвертер JSON↔CSV, CSV→XLSX")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # json → csv
    json2csv_parser = sub.add_parser("json2csv")
    json2csv_parser.add_argument("--in", dest="input", required=True, help="Путь к входному JSON")
    json2csv_parser.add_argument("--out", dest="output", required=True, help="Путь к выходному CSV")
    json2csv_parser.set_defaults(func=lambda args: json_to_csv(args.input, args.output))

    # csv → json
    csv2json_parser = sub.add_parser("csv2json")
    csv2json_parser.add_argument("--in", dest="input", required=True, help="Путь к входному CSV")
    csv2json_parser.add_argument("--out", dest="output", required=True, help="Путь к выходному JSON")
    csv2json_parser.set_defaults(func=lambda args: csv_to_json(args.input, args.output))

    # csv → xlsx
    csv2xlsx_parser = sub.add_parser("csv2xlsx")
    csv2xlsx_parser.add_argument("--in", dest="input", required=True, help="Путь к входному CSV")
    csv2xlsx_parser.add_argument("--out", dest="output", required=True, help="Путь к выходному XLSX")
    csv2xlsx_parser.set_defaults(func=lambda args: csv_to_xlsx(args.input, args.output))

    args = parser.parse_args()

    # Проверка существования входного файла
    input_path = Path(args.input)
    if not input_path.exists():
        parser.error(f"Входной файл '{args.input}' не найден")

    # Вызов функции для выбранной команды
    args.func(args)



if __name__ == "__main__":
    main()
