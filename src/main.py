from pathlib import Path
from excel_reader import  read_excel_lines
from header_parser import extract_header
from customer_parser import extract_customer



BASE_DIR = Path(__file__).resolve().parent.parent

file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"
# file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"


result = read_excel_lines(file)
print(result["header_lines"])
header = extract_header(result["header_lines"])
# customer = result["customer_lines"]
print(header)
# print(customer)