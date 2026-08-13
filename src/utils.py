import re
from datetime import datetime
from config import tax_codes

def parse_amount(value):
    #covert string to float, handle different formats like 138.024,00 or 138,024.00
    if not value:
        return None
    value = str(value).strip()
    # contains both "." and ","
    if "." in value and "," in value:
        # European format if the last "," is after the last "."
        if value.rfind(",") > value.rfind("."):
            # European format: 138.024,00 -> 138024.00
            # remove all "." and replace "," with "."   
            value = value.replace(".", "")
            value = value.replace(",", ".")
        else:
            # UK format if the last "." is after the last ","
            # UK format: 138,024.00 -> 138024.00
            # remove all "," and keep "." as decimal separator
            value = value.replace(",", "")

    # only contains ","
    # replace "," with "." to convert to float
    elif "," in value:
        value = value.replace(",", ".")

    try:
        # only contains "."
        # keep "." as decimal separator, no change needed
        return float(value)
    # handle ValueError if the string cannot be converted to float
    except ValueError:
      return None

def extract_date(date):
    # 数字格式: 23.10.2026
    pattern =re.compile(r'(\d{1,2})[./-](\d{1,2})[./-](\d{4})')
    if not date:
        return None
   
    match = pattern.search(date)
    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)
        
        # 验证日期
        try:
            date_obj = datetime(int(year), int(month), int(day))
            date_result=f"{year}-{int(month):02d}-{int(day):02d}"
            return date_result
            
        except ValueError:
            # 无效日期（如 31.02.2026）
            return None

def is_item_line(line):
    # Item line: contain Pos nr at begin, tax code at end.
    # ?: non-capturing group, \b word boundary, \d{3} tax code
    pattern = re.compile(r'^(\d+(?:\.\d+)*)\s+.*?\b(\d{3})$') 
    # If the line doesn't match the expected format, or the tax code is invalid, return None
    if pattern.search(line.strip()):
        if pattern.search(line.strip()).group(2) in tax_codes:
            return True
    return False
     