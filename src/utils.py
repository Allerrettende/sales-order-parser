import re

def parse_amount(value):

    if not value:
        return None

    value = value.strip()


    # 同时包含 . 和 ,
    if "." in value and "," in value:

        # 最后出现的位置决定小数点
        if value.rfind(",") > value.rfind("."):
            # 欧洲格式
            # 138.024,00
            value = value.replace(".", "")
            value = value.replace(",", ".")

        else:
            # 英文格式
            # 138,024.00
            value = value.replace(",", "")


    # 只有逗号
    elif "," in value:

        # 认为是小数
        # 319,00
        value = value.replace(",", ".")


    # 只有点
    # 319.00
    # 不处理


    return float(value)


from datetime import datetime

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