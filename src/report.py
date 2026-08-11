
def print_order_summary(orders_data):
    """
    打印订单摘要信息
    """
    if not orders_data:
        print("No orders to summarize")
        return
    
    print("\n" + "="*80)
    print("📊 ORDER SUMMARY")
    print("="*80)
    
    total_orders = len(orders_data)
    total_items = sum(len(order['items']) for order in orders_data)
    total_amount = sum(order['header'].get('subtotal_amount', 0) for order in orders_data)
    
    print(f"Total Orders: {total_orders}")
    print(f"Total Items: {total_items}")
    print(f"Total Amount: {total_amount:,.2f}")
    print(f"Currency: {orders_data[0]['header'].get('currency', 'N/A') if orders_data else 'N/A'}")
    
    print("\nOrder List:")
    print("-"*80)
    for order in orders_data:
        header = order['header']
        customer = order['customer']
        print(f"Order: {header.get('sales_order_no', 'Unknown')} | "
              f"Customer: {customer.get('customer_name', 'Unknown')} | "
              f"Items: {len(order['items'])} | "
              f"Amount: {header.get('subtotal_amount', 0):,.2f}")

