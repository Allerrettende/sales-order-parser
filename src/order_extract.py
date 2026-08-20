import re
import openpyxl

def read_excel_lines(file_path):

    """
    Read Excel file exported from PDF.
    Return all lines as a list of strings, not stripped, only skipping empty lines
    """
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb.active
    all_lines = []
    for row in ws.iter_rows():
        value = row[0].value
        if value is None or str(value).strip() == "":
            continue 
        all_lines.append(str(value))
    wb.close()
    return all_lines

def extract_customer_lines(all_lines):
    # return stripped lines that are likely to contain customer information

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
    # return stripped lines that are likely to contain header information
    header_lines=[]
    #header lines include all lines except blank lines,
    for line in all_lines:
        line=line.strip()
        if line:
            header_lines.append(line)

    return header_lines

def extract_item_lines(lines):
    #return stripped lines that are likely to contain item information, and details, with error handling and logging
    item_lines = []
    starting = False
    
    for line_num, line in enumerate(lines, 1):

        if is_end_line(line):
            # print(f"✅ 找到结束标记在第 {line_num} 行: {repr(line)}")
            break

        # Start line
        if is_start_line(line):
            # print(f"✅ 找到开始标记在第 {line_num} 行")
            starting = True
            continue
        # skip if not start
        if not starting:
            continue

        # line should be excluded, such as line with lot space prefix, page break etc.
        if is_exlude_line(line):
            # print(f"⏭️  排除行 [{line_num}]: {repr(line.strip()[:50])}")
            continue
       
        # Collect group header line, remark of group, product lines, details of prduct, group footer line, and details of group, such as discount.
        item_lines.append(line.strip())

        # below are for test purpose

        # if is_product_line(line):
        #     # if line.split()[1]=="Discount":
        #     #     print(line.split())
        #     # print(f"✅ 产品行 [{line_num}]: {repr(line.strip()[:60])}")

        # group line
        # if is_group_head_line(line):
        #     # print(f"⏭️  group行 [{line_num}]: {repr(line.strip()[:50])}")

    # print(f"\n总共收集了 {len(item_lines)} 行")
    
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
 
def is_exlude_line(line):
        
    # lines not like defined before, and should be eliminated.
    exclude_patterns = [
        re.compile(r'Balance\s+'),      # contains 'Balance' when there are more than on page.
        re.compile(r'Subtotal\s+'),     # contains 'Subtotal' 
        re.compile(r'Order Confirmation\s+\d{4}-\d{6}'),     # contains 'Order Confirmation 2024-864223        Page      2 From 2' 
        re.compile(r'Pos\.*Unit.*Price', re.IGNORECASE), # item header lines in next page, such as: "Pos. Unit Price"
        re.compile(r'Pos\..*Numbe', re.IGNORECASE), # header line, such as 'Pos.        Numbe'
        re.compile(r'Unit.*Price', re.IGNORECASE), # header line, such as 'Pos.        Numbe'Unit.*Price
        re.compile(r'_x000C_'),          # page break line in excel, should be excluded.
        # re.compile(r'^[-*#].*'),         # # remark: "*** Lead time: 1 week.***"
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

# some statement looks like details but not belong to item line.
# when gather the details, should exclude this line.
def is_remark_line(line): 

    # remark: "         *** Lead time: 1 week.***"
    pattern = re.compile(r'^[*#].*')
    if pattern.search(line.strip()):
        return True
    return False



