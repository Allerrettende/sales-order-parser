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
        # skip if value is None or str(value).strip() == "":
        if value is None or str(value).strip() == "":
            continue 
        all_lines.append(str(value))

    return all_lines

def extract_customer_lines(all_lines):

    customer_lines = []
    # Customer block is usually within first 8 rows
    # in case the lines are lower than 8, ignore the lines are not belong to customer infor.
    for line in all_lines[:8]:
        leading_spaces = (len(line) - len(line.lstrip()) )
        # skip the line has more than 20 spaces presuffix.
        if leading_spaces >= 20:
            continue
        line=line.strip()
        line = re.split(r"\s{5,}",line)[0]
        if line:
            customer_lines.append(line)

    return customer_lines
    
def extract_header_lines(all_lines):

    header_lines=[]
    #header lines include all lines except blank lines,
    for line in all_lines:
        line=line.strip()
        if line:
            header_lines.append(line)

    return header_lines

def extract_item_lines(lines):
 
    item_lines = []
    starting = False
    belong_item = False
    
    for line_num, line in enumerate(lines, 1):

        if is_end_line(line):
            print(f"✅ 找到结束标记在第 {line_num} 行: {repr(line)}")
            break

        # Start line
        if is_start_line(line):
            print(f"✅ 找到开始标记在第 {line_num} 行")
            starting = True
            continue
        # skip if not start
        if not starting:
            continue

        # line should be excluded, such as line with lot space prefix, page break etc.
        if is_exlude_line(line):
            print(f"⏭️  排除行 [{line_num}]: {repr(line.strip()[:50])}")
            continue

        # group line
        if is_group_line(line):
            print(f"⏭️  跳过group行 [{line_num}]: {repr(line.strip()[:50])}")
            belong_item = False
            continue
        
        # Item collection: check if it is item line, 
        # if yes, collect it; if not, check if it is details line, if yes, collect it; if not, skip it.
        if is_item_line(line):
            print(f"✅ 产品行 [{line_num}]: {repr(line.strip()[:60])}")
            item_lines.append(line.strip())
            belong_item = True
            belong_group = False

        else:
            # item details collection base on status machine: 
            # check status machine: if last line is item line, then next line is details line, if not, skip it.
            if not belong_item:
                print(f"⏭️  跳过group remark [{line_num}]: {repr(line.strip()[:50])}")
                continue
            # check if it is remark line etc.
            if is_remark_line(line):
                print(f"📝 备注行 [{line_num}]: {repr(line.strip()[:60])}")
                continue
            # Just conduct before one item was collected, to avoid adding other remarks before first item.
            if belong_item:
                print(f"📝 描述行 [{line_num}]: {repr(line.strip()[:60])}")
                item_lines.append(line.strip())
    
    print(f"\n总共收集了 {len(item_lines)} 行")
    
    return item_lines

def is_end_line(line):
    # contains 'Subtotal' + " " + Currency.
    pattern = re.compile(r'Subtotal\s+\S{3}\s+', re.IGNORECASE)
    if pattern.search(line):
        return True
    return False

def is_start_line(line):
    # contains 'Pos. Item Description'
    pattern = re.compile(r'^Pos\.\s+Item\s+Description', re.IGNORECASE)
    if pattern.search(line.strip()):
        return True
    return False
 
def is_group_line(line):
    # group line（such as: "1        - Zeochem Donghai "）
    # group line（such as: "1        * Zeochem Donghai "）
    # group line（such as: "1        # Zeochem Donghai "）
    pattern = re.compile(r'^\d+\s+[-,*,#].*$')
    if pattern.search(line.strip()):
        return True
    return False

def is_item_line(line):
    # Item line: contain Pos nr at begin, tax code at end.
    pattern = re.compile(r'^\d+(?:\.\d+)*.*?\b\d{3}$')
    if pattern.search(line.strip()):
        return True
    return False

def is_exlude_line(line):
        
    # lines not like defined before, and should be eliminated.
    exclude_patterns = [
        re.compile(r'^\s{30,}.*$'),      # more than 30 spaces at the beginning of the line
        re.compile(r'^Balance\s+'),      # contains 'Balance'
        re.compile(r'Subtotal\s+'),     # contains 'Subtotal' 
        re.compile(r'Pos.\s+.Item\s+', re.IGNORECASE), # item header lines in next page, such as: "Pos. Item Description"
        re.compile(r'_x000C_'),          # page break line in excel, should be excluded.
    ]

    should_exclude = False
    for pattern in exclude_patterns:
        
        if pattern.search(line) or pattern.match(line):
            # print(f"⏭️  exclude : {repr(pattern)}")
            should_exclude = True
            break

    if should_exclude:
        return True
    return False

# some statement looks like details nut not belong to item line.
# when gather the details, should exclude this line.
def is_remark_line(line): 

    # remark: "         *** Lead time: 1 week.***"
    pattern = re.compile(r'^[-,*,#].*')
    if pattern.search(line.strip()):
        return True
    return False


# 被其他模块调用时，直接返回 lines；被 main.py 调用时，打印 lines。
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent
    # file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"
    file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx"
    # file = BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864118.xlsx"
    file = BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864136.xlsx"
    order_data = read_excel_lines(file)
    
    # customer_lines=extract_customer_lines(order_data)
    # print(customer_lines)
    hd=extract_item_lines(order_data)
    print(hd)