import re
from utils import parse_amount

def extract_header(lines):
    
    header = {
        "sales_order_no": None,
        "document_date": None,
        "customer_no": None,
        "agent": None,
        "reference_quote_no": None,
        "currency": None,
        "subtotal_amount": None,

    }

    # print("Extracting header information from lines...")
    for line in lines:
        
        line = line.strip()
        match = re.search(
            r"DOCUMENT NO\.\s+(\S+)",
            line
        )
        if match:
            header["sales_order_no"] = match.group(1)


        match = re.search(
            r"Date\s+(\d{2}\.\d{2}\.\d{4})",
            line
        )
        if match:
            header["document_date"] = match.group(1)


        match = re.search(
            r"CUSTOMER NO\.\s+(\S+)",
            line
        )
        if match:
            header["customer_no"] = match.group(1)


        match = re.search(
            r"Agent\s+(.+)",
            line
        )
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


   

