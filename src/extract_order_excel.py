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
    customer_lines = []

    # Customer block is usually within first 6 rows
    for line in all_lines[:6]:
        leading_spaces = (
            len(line)
            -
            len(line.lstrip())
        )

        # Ignore right-side header lines
        if leading_spaces >= 10:
            continue

        customer_area = re.split(
            r"\s{5,}",
            line.strip()
        )

        customer_line = (
            customer_area[0]
            .strip()
        )

        if customer_line:
            customer_lines.append(
                customer_line
            )

    return {
        "all_lines": all_lines,
        "customer_lines": customer_lines
    }

# 被其他模块调用时，直接返回 lines；被 main.py 调用时，打印 lines。
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent
    file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"
    # file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"

    result = read_excel_lines(file)
    print(type(result))
    print(result["all_lines"])