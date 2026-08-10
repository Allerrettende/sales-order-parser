import re
from utils import parse_amount, extract_date
from config import tax_codes

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

# ************ Parse item lines, including product lines and detail lines ************

def parse_item(line):

    """
    Parse a product line into a structured dictionary.
    item details will be processed separately.
    the line has already been stripped and cleaned, and is a product line
   
    """
    parts=line.split()
    # parse pos_number, item description, quantity, unit, unit_price, amount, tax_code from parts
    return {
        "pos_number": parts[0],
        "item_description": " ".join(parts[1:-5]),
        "item_details": [],
        "quantity": parse_amount(parts[-5]),
        "unit": parts[-4],
        "unit_price": parse_amount(parts[-3]),
        "amount": parse_amount(parts[-2]),
        "tax_code": parts[-1],
    }
 
 # parse item lines that have been verified through order extraction, only product lines and item details lines are included, other lines have been eliminated.
 # The item details are the lines after the product line until the next product line or end of file.
 # return a generator of parsed items, each item is a dictionary with keys: pos_number, item_description（list), item_details, quantity, unit, unit_price, amount, tax_code.
def gen_parse_items(lines):

    current_item = None
    for line in lines:
        match = re.match(r'^(\d+(?:\.\d+)*).*?\b(\d{3})$', line)
        if match:
            if current_item:
                # return the current parsed item before starting a new one
                # the current_item is a dictionary for last product line, and the item_details is a multi-line string below product line.
                yield current_item
            # start parsing a new item
            current_item = parse_item(line)
        else:
            if current_item:
                current_item["item_details"].append(line)
    # return the last parsed item if any
    if current_item:
        yield current_item


if __name__ == "__main__":
    # 测试数据
    test_lines = [
        "1.12 Product A 999 pcs 10.50 1000 999",
        "This is a detailed description of product A",
        "It has multiple lines of description",
        "2.0 test 10 78",
        "this is a description for product 2",

    ]
    
       
    for item in gen_parse_items(test_lines):
        print(f"\nItem found:")
        for key, value in item.items():
            if value:
                print(f"  {key}: {value}")
 
