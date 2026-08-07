import re
from utils import parse_amount

def parse_header(lines):
    
    header = {
        "document_no": None,
        "document_date": None,
        "customer_no": None,
        "agent": None,
        "reference_quote_no": None,
        "currency": None,
        "subtotal_amount": None,
    }

    # print("Extracting header information from lines...")
    
    line_num=0
    for line in lines:
        line_num+=1
        match = re.search(r"DOCUMENT NO\.\s+(\S+)",line)
        if match:
            header["document_no"] = match.group(1)

        # 多种日期格式: 3.10.2026 或 03/10/2026 或 3-10-2026 等(日.月.年)
        # 匹配 "Date" 后面的日期
        pattern = r'Date\s+(\d{1,2})[./-](\d{1,2})[./-](\d{4})'
        match = re.search(pattern, line, re.IGNORECASE)
        if match and line_num<6: # Date is in line 4
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            # 标准化日期格式
            header["document_date"] = f"{year}-{int(month):02d}-{int(day):02d}"

        match = re.search(
            r"CUSTOMER NO\.\s+(\S+)",line)
        if match:
            header["customer_no"] = match.group(1)

        match = re.search(r"Agent\s+(.+)",line)
        if match:
            header["agent"] = match.group(1).strip()

        match = re.search(
            r"Reference Quote\s+(\d{4}-\d+)",
            line
        )
        if match:
            header["reference_quote_no"] = match.group(1)

        match = re.search(
            r"Subtotal\s+([A-Z]{3})\s+([\d.,]+)",
            line
        )
        if match:
            header["currency"] = match.group(1)
            header["subtotal_amount"] = parse_amount(match.group(2))

    return header


# # *********** customer infor structure *********
# # Name1
# Name2(Option)
# Address1
# Address2(Option)
# Zip + City, Upcase, missing sometime
# Country, Upcase, missing sometime
#  #*************************************************

def parse_customer(lines):

    customer = {
        "customer_name": None,
        "customer_address": None,
        "customer_postcode": None,
        "customer_city": None,
        "customer_country": None,
    }


   
    last_line_number=len(lines)-1
    customer_name=lines[0]
    if is_company_name_line(lines[1]):
        customer_name=customer_name + " " + lines[1]
    # Country
    if is_country_line(lines[-1]):
        customer["customer_country"] = lines[-1]

        


    for line in lines:

        customer["customer_name"]=customer_name

        # Postcode + City
        pattern = r"^(\d{5,6})\s+(.+)"
        match = re.match(pattern,line)
        if match:
            customer["customer_postcode"] = match.group(1)
            customer["customer_city"] = match.group(2)




        

    return customer

def is_company_name_line(line):
    company_keywords = [
        "LTD",
        "LIMITED",
        "GMBH",
        "INC",
        "LLC",
        "CORP",
        "CO."
    ]

    line_upper = line.upper()
    # 检查是否包含任何国家名称
    for co in company_keywords:
        if co in line_upper:
            return True
    return False


def is_country_line(line):

    # 定义国家列表（全大写）
    countries_list = ['CHINA', 'USA', 'GERMANY', 'UK', 'FRANCE', 'JAPAN', 'CANADA', 'AUSTRALIA']
    line_upper = line.upper()

    # 检查是否包含任何国家名称
    for country in countries_list:
        if country in line_upper:
            return True
    return False
 
if __name__ == "__main__":
    cline="uddsad CHIN ltd"
    if is_company_name_line(cline):
        print(cline)
    else: print("Not")