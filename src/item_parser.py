import re
from config import tax_codes
from utils import parse_amount

def extract_items(lines):
    print("Extracting item information from lines...")
    item= {
        "pos_number": None,
        "item_description": None,
        "quantity": None,
        "unit": None,
        "unit_price": None,
        "amount": None,
        "tax_code": None,
    }

    current_item=None
    for line in lines:
        
        line = line.strip()
  




def extract_tax_code(line):
    
    tc = line.strip().split()[-1]
    if tc in tax_codes: # tax_codes defined in config.py
        return tc
    return None

def extract_pos(line):
    match = re.match(
        r"^\s*(\d+(?:\.\d+)?)\s+",
        line
    )
    if match:
        return match.group(1)
    return None

def extract_values(line):

    parts = line.strip().split()

    return {
        "quantity": parse_amount(parts[-5]),
        "unit": parts[-4],
        "unit_price": parse_amount(parts[-3]),
        "amount": parse_amount(parts[-2]),
        "tax_code": parts[-1], # [-1] TC
    }

def extract_description(line):

    parts = line.strip().split()
    quantity_index = -5
    description = " ".join(
        parts[1:quantity_index]
    )
    return description

# gather information of item master line
def extract_item(line):

    if not extract_tax_code(line):
        return None
    
    item = {}
    item["pos_number"] = extract_pos(line)
    item["item_description"] = extract_description(line)
    values = extract_values(line)
    item.update(values)
    return item



if __name__ == "__main__":
    item_line="1.1      Audiocode Mediant 1000B                      1,00 Piece               30.350,00              30.350,00 903"
    print(extract_item(item_line))
