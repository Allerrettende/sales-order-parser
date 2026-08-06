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