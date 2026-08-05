import re
import openpyxl
from pathlib import Path

def read_excel_lines(file_path):
   
    # Read Excel file exported from PDF.
    # Return all non-empty cells in first column.
  
    # openpyxl 比 pandas.read_excel 更直观。因为读的不是分析表。
    wb = openpyxl.load_workbook(
        file_path,
        data_only=True
    )
    ws = wb.active
    all_lines = []
 
    # 读取所有A列
    for row in ws.iter_rows():
        value = row[0].value
        if value:
            all_lines.append(str(value).strip())

    # Obtain customer basic info from the first 6 lines, which are usually in the left area of the page.
    customer_lines = []
    header_lines = []
    # 前6行：客户+Header区域
    for line in all_lines[:6]:
        left, right = split_left_right(line)
        if left:
            customer_lines.append(left)
        if right:
            header_lines.append(right)
    return {
        "all_lines": all_lines,
        "customer_lines": customer_lines,
        "header_lines": header_lines
    }

    
def split_left_right(line):

    # Split PDF converted line into left and right area.
    parts = re.split(
        r"\s{5,}",
        line
    )
    left = parts[0].strip()
    print(parts[0])
    if len(parts) > 1:
        print(parts[1])

    # print(parts[1])
    right = ""
    # print(len(parts))
    if len(parts) > 1:
        
        right = " ".join(
            parts[1:]
        ).strip()
        # print(right)

    return left, right

# 被其他模块调用时，直接返回 lines；被 main.py 调用时，打印 lines。
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent
    file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"

    result = read_excel_lines(file)
    print(result["header_lines"])
    # print(result["customer_lines"])