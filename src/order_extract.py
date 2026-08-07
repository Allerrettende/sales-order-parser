import re
import openpyxl
from pathlib import Path

def read_excel_lines(file_path):

    """
    Read Excel file exported from PDF.
    Return:
        all_lines: with all lines in the first column of the Excel file.
        customer_lines: with lines containing customer information.
    """
    wb = openpyxl.load_workbook(
        file_path,
        data_only=True
    )

    ws = wb.active
    all_lines = []
    # Keep original text format
    for row in ws.iter_rows():
        value = row[0].value
        if value:
            all_lines.append(
                str(value)
            )

    return all_lines

def extract_customer_lines(all_lines):

    customer_lines = []
    # Customer block is usually within first 6 rows
    for line in all_lines[:6]:
        leading_spaces = (len(line) - len(line.lstrip()) )
        # in case the lines are lower than 6, ignore the lines are not belong to customer infor.
        if leading_spaces >= 20:
            continue
        line=line.strip()
        line = re.split(r"\s{5,}",line)[0]
        if line:
            customer_lines.append(line)

    return customer_lines
    
def extract_header_lines(all_lines):

    header_lines=[]
    #header block includes top-right area, and subtotal amount line, quote line.
    for line in all_lines[:20]:
        line=line.strip()
        if line:
            header_lines.append(line)
        
    return header_lines


# 被其他模块调用时，直接返回 lines；被 main.py 调用时，打印 lines。
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent
    # file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"
    # file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"
    file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864118.xlsx"
    file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864136.xlsx"
    order_data = read_excel_lines(file)
    
    # customer_lines=extract_customer_lines(order_data)
    # print(customer_lines)
    hd=extract_header_lines(order_data)
    print(hd)