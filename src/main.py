from pathlib import Path
from unittest import result
from order_extract import  read_excel_lines
from order_parser import extract_header
from customer_parser import extract_customer
from item_parser import extract_item


BASE_DIR = Path(__file__).resolve().parent.parent

file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"
# file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864136.xlsx"
# file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864118.xlsx"

data = read_excel_lines(file)
# header = extract_header(data["all_lines"])
# print(header)


# line=data["all_lines"][18]
# print(line)
# item = extract_item(line)
# print(item)

