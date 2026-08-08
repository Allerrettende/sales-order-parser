from pathlib import Path
# from unittest import result
from order_extract import  read_excel_lines, extract_customer_lines, extract_header_lines
from order_parser import parse_header,parse_customer
# from customer_parser import extract_customer
# from item_parser import extract_item

BASE_DIR = Path(__file__).resolve().parent.parent

file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864136.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864118.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059_noContry.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864258.xlsx"

data = read_excel_lines(file)
header_lines=extract_header_lines(data)
header = parse_header(header_lines)
print(header)

customer_line=extract_customer_lines(data)
customer=parse_customer(customer_line)
print(customer)


