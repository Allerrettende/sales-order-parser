from pathlib import Path
# from unittest import result
from order_extract import  extract_item_lines, read_excel_lines, extract_customer_lines, extract_header_lines
from order_parser import gen_parse_items, parse_header,parse_customer

BASE_DIR = Path(__file__).resolve().parent.parent

file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864136.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864118.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059_noContry.xlsx"
file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864258.xlsx"

data = read_excel_lines(file)

customer_line=extract_customer_lines(data)
customer=parse_customer(customer_line)
print(customer)

header_lines=extract_header_lines(data)
header = parse_header(header_lines)
print(header)

item_lines = extract_item_lines(data)
items_generator= gen_parse_items(item_lines)

# print(list(items_generator))  # This will exhaust the generator, so we can't iterate over it again
for item in items_generator:
    print(f"\nItem found:")
    for key, value in item.items():
        if value:
            print(f"  {key}: {value}")




