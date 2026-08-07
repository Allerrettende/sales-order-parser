import re


def parse_customer_v1(customer_lines):

    customer = {
        "customer_name": None,
        "customer_address": None,
        "customer_postcode": None,
        "customer_city": None,
        "customer_country": None,
    }


    # remove empty lines
    # use list comprehension to filter out empty lines and strip whitespace
    lines = [
        line.strip()
        for line in customer_lines
        if line.strip()
    ]

    if len(lines) < 3:
        return customer

    # Company name
    customer["customer_name"] = lines[0]

    # Find postcode + city
    zip_index = None

    for i, line in enumerate(lines):

        if re.match(
            r"^\d{5,6}\s+",
            line
        ):
            zip_index = i
            break


    if zip_index is None:
        return customer


    # Address
    address_lines = lines[1:zip_index]

    customer["customer_address"] = (
        " ".join(address_lines)
        if address_lines
        else None
    )


    # Postcode + City
    match = re.match(
        r"^(\d{5,6})\s+(.+)",
        lines[zip_index]
    )

    if match:

        customer["customer_postcode"] = match.group(1)

        customer["customer_city"] = match.group(2)


    # Country
    if zip_index + 1 < len(lines):

        customer["customer_country"] = (
            lines[zip_index + 1]
        )


    return customer