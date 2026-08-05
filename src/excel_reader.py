import re
import openpyxl
from pathlib import Path


def read_excel_lines(file_path):
    """
    Read Excel file exported from PDF.
    Return all non-empty cells in first column.
    """
    # openpyxl 比 pandas.read_excel 更直观。因为读的不是分析表。
    wb = openpyxl.load_workbook(
        file_path,
        data_only=True
    )
    ws = wb.active
    lines = []
    customer_lines = []

    
    for row in ws.iter_rows():
        value = row[0].value

        if value:
            lines.append(str(value).strip())

    # Obtain customer basic info from the first 6 lines, which are usually in the left area of the page.

    for line in lines[:6]:

        customer_basic_info = split_left_right(line)

        if customer_basic_info[0]:
            customer_lines.append(customer_basic_info[0])

    # return {
    #     "all_lines": lines,
    #     "customer_lines": customer_lines
    # }

    return lines,customer_lines
    
def split_left_right(line):
    # Split PDF converted line into left and right area.
    left=[]
    parts = re.split(
        r"\s{5,}",
        line
    )
    left = parts[0].strip()
    print(left)
    return left


# 被其他模块调用时，直接返回 lines；被 main.py 调用时，打印 lines。
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent
    file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"

    lines, customer_lines = read_excel_lines(file)
    for line in lines:
        print(line)
    # for line in customer_lines:
    #     print(line)