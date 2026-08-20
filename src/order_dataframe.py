import pandas as pd

def orders_to_dataframe(orders_data):
    """
    Convert a list that restored all orders to DataFrame.
    
    """
    if not orders_data:
        return pd.DataFrame()
    
    all_rows = []
    
    for order_data in orders_data:
        header = order_data['header']
        customer = order_data['customer']
        items = order_data['items']
        
        # 为每个订单项创建一行数据
        for item in items:
            row = {
                # 表头信息
                "sales_order_no": header.get('sales_order_no', ''),
                "document_date": header.get('document_date', ''),
                "customer_no": header.get('customer_no', ''),
                "agent": header.get('agent', ''),
                "reference_quote_no": header.get('reference_quote_no', ''),
                "currency": header.get('currency', ''),
                "subtotal_amount": header.get('subtotal_amount', 0),
                
                # 客户信息
                "customer_name": customer.get('customer_name', ''),
                "customer_address": customer.get('customer_address', ''),
                "customer_postcode": customer.get('customer_postcode', ''),
                "customer_city": customer.get('customer_city', ''),
                "customer_country": customer.get('customer_country', ''),
                
                # 订单项信息
                "pos_number": item.get('pos_number', ''),
                "item_description": item.get('item_description', ''),
                "item_details": '\n'.join(item.get('item_details', [])) if item.get('item_details') else '',
                "quantity": item.get('quantity', 0),
                "unit": item.get('unit', ''),
                "unit_price": item.get('unit_price', 0),
                "amount": item.get('amount', 0),
                "discount":item.get('discount',0),
                "tax_code": item.get('tax_code', ''),
            }
            all_rows.append(row)
    
    # 创建 DataFrame
    df = pd.DataFrame(all_rows)
    
    # 定义列的显示顺序
    column_order = [
        "sales_order_no",
        "document_date",
        "customer_no",
        "customer_name",
        "customer_address",
        "customer_postcode",
        "customer_city",
        "customer_country",
        "agent",
        "reference_quote_no",
        "currency",
        "subtotal_amount",
        "pos_number",
        "item_description",
        "item_details",
        "quantity",
        "unit",
        "unit_price",
        "amount",
        "discount",
        "tax_code",
    ]
    
    # 只保留存在的列并按指定顺序排列
    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns]
    
    return df