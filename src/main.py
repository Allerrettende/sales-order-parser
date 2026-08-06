from pathlib import Path
from unittest import result
from extract_order_excel import  read_excel_lines
from header_parser import extract_header
from customer_parser import extract_customer
from item_parser import extract_item


BASE_DIR = Path(__file__).resolve().parent.parent

file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"
# file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"

data = read_excel_lines(file)
# header = extract_header(data["all_lines"])
# customer = extract_customer(data["customer_lines"])
# print(header)
# print(customer)

line=data["all_lines"][18]
print(line)
# item = extract_item(line)
# print(item)

