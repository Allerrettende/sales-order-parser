import re
from datetime import datetime

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

if __name__ == "__main__":
    test_values = [
        "138.024,00",
        "138,024.00",
        "319,00",
        "319.00",
        "1,234,567.89",
        "1.234.567,89",     
        "1234567.89",
        "1234567,89",
    ]

    for val in test_values:
        parsed = parse_amount(val)
        print(f"Original: {val} -> Parsed: {parsed}")     




    # 使用示例


    test_texts = [
        "Date 3.10.2026",
        "Date 03/10/2026",
        "Date 3-Oct-2026",
        "Date 3-6-2026",
        "Date 31.12.2026",
        "Date 31.02.2026",  # 无效日期
    ]

    for text in test_texts:
        result = extract_date(text)
        print(result)
        if result:
            print(f"✅ {text} ")
        else:
            print(f"❌ {text} -> 无效日期")          