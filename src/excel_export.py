import pandas as pd


def orders_to_dataframe(orders_data):
    """
    将订单数据列表转换为 DataFrame
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
                "tax_code": item.get('tax_code', ''),
            }
            all_rows.append(row)
    
    # 创建 DataFrame
    df = pd.DataFrame(all_rows)
    
    # 重新排列列的顺序
    columns = [
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
        "tax_code",
    ]
    
    # 只保留存在的列
    existing_columns = [col for col in columns if col in df.columns]
    df = df[existing_columns]
    
    return df

def export_to_excel_with_formatting(df, output_path):
    """
    将 DataFrame 导出为格式化的 Excel 文件
    """
    if df.empty:
        print("❌ No data to export!")
        return
    
    # 创建 Excel writer
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # 写入数据
        df.to_excel(writer, sheet_name='Orders', index=False)
        
        # 获取工作表
        workbook = writer.book
        worksheet = writer.sheets['Orders']
        
        # 设置列宽
        column_widths = {
            'A': 18,  # sales_order_no
            'B': 15,  # document_date
            'C': 15,  # customer_no
            'D': 30,  # customer_name
            'E': 35,  # customer_address
            'F': 15,  # customer_postcode
            'G': 20,  # customer_city
            'H': 15,  # customer_country
            'I': 18,  # agent
            'J': 20,  # reference_quote_no
            'K': 12,  # currency
            'L': 18,  # subtotal_amount
            'M': 12,  # pos_number
            'N': 40,  # item_description
            'O': 12,  # quantity
            'P': 12,  # unit
            'Q': 15,  # unit_price
            'R': 15,  # amount
            'S': 12,  # tax_code
        }
        
        for col_letter, width in column_widths.items():
            worksheet.column_dimensions[col_letter].width = width
        
        # 设置表头样式
        from openpyxl.styles import Font, Alignment, PatternFill
        
        header_font = Font(name='Arial', size=10, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        for cell in worksheet[1]:  # 第一行是表头
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # 设置数据格式
        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(horizontal='left', vertical='center')
                
                # 数值列右对齐
                col_letter = cell.column_letter
                if col_letter in ['L', 'O', 'Q', 'R']:  # 金额和数量列
                    cell.alignment = Alignment(horizontal='right', vertical='center')
                    if col_letter in ['L', 'Q', 'R']:  # 金额列
                        cell.number_format = '#,##0.00'
        
        # 冻结首行
        worksheet.freeze_panes = 'A2'

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