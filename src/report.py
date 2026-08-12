
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

#   summary
def export_summary_statistics(orders_data, output_dir):
    """
    导出订单统计摘要
    """
    if not orders_data:
        return
    
    summary_data = []
    
    for order_data in orders_data:
        header = order_data['header']
        customer = order_data['customer']
        items = order_data['items']
        
        summary = {
            'Sales Order No': header.get('sales_order_no', ''),
            'Customer Name': customer.get('customer_name', ''),
            'Total Items': len(items),
            'Total Amount': header.get('subtotal_amount', 0),
            'Currency': header.get('currency', ''),
            'Document Date': header.get('document_date', ''),
            'Customer No': header.get('customer_no', ''),
            'Agent': header.get('agent', ''),
        }
        summary_data.append(summary)
    
    summary_df = pd.DataFrame(summary_data)
    
    # 导出统计摘要
    summary_path = output_dir / "order_summary.xlsx"
    with pd.ExcelWriter(summary_path, engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # 设置格式
        workbook = writer.book
        worksheet = writer.sheets['Summary']
        
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column].width = adjusted_width
        
        # 添加统计信息
        summary_row = len(summary_df) + 3
        worksheet.cell(row=summary_row, column=1, value="Total Orders:")
        worksheet.cell(row=summary_row, column=2, value=len(summary_df))
        
        total_amount = summary_df['Total Amount'].sum()
        worksheet.cell(row=summary_row+1, column=1, value="Total Amount:")
        worksheet.cell(row=summary_row+1, column=2, value=total_amount)
        worksheet.cell(row=summary_row+1, column=2).number_format = '#,##0.00'
    
    print(f"📊 Summary statistics exported to: {summary_path}")