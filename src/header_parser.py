import re


def extract_header(lines):

    header = {
        "Sales_Order_No": None,
        "Document_Date": None,
        "Customer_No": None,
        "Agent": None,
        "Reference_Quote_No": None,
    }


    for line in lines:

        line = line.strip()


        match = re.search(
            r"DOCUMENT NO\.\s+(\S+)",
            line
        )
        if match:
            header["Sales_Order_No"] = match.group(1)


        match = re.search(
            r"Date\s+(\d{2}\.\d{2}\.\d{4})",
            line
        )
        if match:
            header["Document_Date"] = match.group(1)


        match = re.search(
            r"CUSTOMER NO\.\s+(\S+)",
            line
        )
        if match:
            header["Customer_No"] = match.group(1)


        match = re.search(
            r"Agent\s+(.+)",
            line
        )
        if match:
            header["Agent"] = match.group(1).strip()


        match = re.search(
            r"Reference Quote\s+(\d{4}-\d+)",
            line
        )
        if match:
            header["Reference_Quote_No"] = match.group(1)


    return header