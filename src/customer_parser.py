import re


def extract_customer(lines):

    customer = {
        "Customer_Name": None,
        "Customer_Address": None,
        "Customer_Postcode": None,
        "Customer_City": None,
        "Customer_Country": None,
    }


    # 找到客户名称行
    start_index = None

    for i, line in enumerate(lines):

        if "Order Confirmation" in line:
            start_index = i
            break


    if start_index is None:
        return customer


    # 客户名称
    name_line = lines[start_index]

    customer["Customer_Name"] = (
        name_line
        .split("Order Confirmation")[0]
        .strip()
    )


    # 收集地址区域
    customer_lines = []

    for line in lines[start_index + 1:]:

        line = line.strip()

        print("DEBUG:", repr(line))
        
        if not line:
            continue

        if "DOCUMENT NO." in line:
            break

        customer_lines.append(line)


    if len(customer_lines) < 2:
        return customer


    # Country
    customer["Customer_Country"] = customer_lines[-1]


    # Zip + City
    zip_city = customer_lines[-2]

    match = re.match(
        r"(\d+)\s+(.+)",
        zip_city
    )

    if match:
        customer["Customer_Postcode"] = match.group(1)
        customer["Customer_City"] = match.group(2)


    # Address
    address_lines = customer_lines[:-2]

    if address_lines:
        customer["Customer_Address"] = " ".join(address_lines)


    return customer