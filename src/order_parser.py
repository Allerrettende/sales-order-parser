import re
from utils import parse_amount, extract_date

def parse_header(lines):

    header = {
        "sales_order_no": None,
        "document_date": None,
        "customer_no": None,
        "agent": None,
        "reference_quote_no": None,
        "currency": None,
        "subtotal_amount": None,
    }

    line_num=0
    for line in lines:
        line_num += 1

        match = re.search(r"DOCUMENT NO\.\s+(\S+)",line)
        if match:
            header["sales_order_no"] = match.group(1)

        # Date format different: 3.10.2026 or 03/10/2026 or 3-10-2026 etc.
        # date should be in format "day month year"
        pattern = r'Date\s+\d{1,2}[./-]\d{1,2}[./-]\d{4}'
        match = re.search(pattern, line)
        if match and line_num<6: # Date is in line 4
            # convert to ISO standard date format
            date_matched=extract_date(match.group(0))
            header["document_date"] = date_matched
            
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
    # customter name always begins from 1st line
    customer_name=lines[0]
    # customer name extends to second line sometime.
    if len(lines)>1 and is_company_suffix_line(lines[1]):
        customer_name +=" " + lines[1]
    customer["customer_name"]=customer_name

    # extract country from bottom to top.
    # extract zip+city afterwards
    # besids above to line, two line for address probably sometime. 
    # address line ended by company line which has company suffix.
    address_parts=[]
    for line in reversed(lines[1:]): # first line is fixed for customer name.
        # Country
        if is_country_line(line):
            customer["customer_country"] = line
            continue

        # post code, and city
        if (result := get_pcode_city(line)):  
            postcode, city = result
            customer["customer_postcode"]=postcode
            customer["customer_city"]=city
            continue

        # if lines are not a country , post code and customer either, lines will be recognized as address line
        if not is_company_suffix_line(line):
            address_parts.append(line)
            address = ' '.join(reversed(address_parts))
            customer["customer_address"] = address
            
    return customer

def get_pcode_city(line):
    # Postcode + City
    pattern = r"^(\d{5,6})\s+(.+)"
    match = re.match(pattern,line)
    if match:
        return match.group(1),match.group(2)
    return None

def is_company_suffix_line(line):
    company_suffixes = [
        "LTD",
        "LIMITED",
        "GMBH",
        "INC",
        "LLC",
        "CORP",
        "CO.",
        "AG",
        "OFFICE",
        "DEPARTMENT"
    ]

    line_upper = line.upper()
    # check last word whether contains company suffix.
    last_word = line.split()[-1].upper().rstrip('.,;:')
    if last_word in company_suffixes:
        return True
    return False

def is_country_line(line):

    # Pre-define counties list.
    countries_list = ['CHINA', 'USA', 'GERMANY', 'UK', 'FRANCE', 'JAPAN', 'CANADA', 'AUSTRALIA']
    line_upper = line.upper()

    # check if pre-defined county name found in line.
    for country in countries_list:
        if line_upper.endswith(country):
        # if line_upper == country:
        # if country in line_upper:
            return True
    return False
 
if __name__ == "__main__":
    cline="uddsad CHIN ltd"
    if is_company_name_line(cline):
        print(cline)
    else: print("Not")