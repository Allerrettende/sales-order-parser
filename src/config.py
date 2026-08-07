tax_codes = {
    "903": {
        "type": "material",
        "description": "Hardware/Material"
    },

    "910": {
        "type": "service",
        "description": "Service"
    },
    "804": {   
        "type": "outsource",
        "description": "Labor/Outsource"
    },
}




if __name__ == "__main__":
    tc="903"

    if tc in tax_codes:
        print(tax_codes[tc]["type"])