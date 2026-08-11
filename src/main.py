from pathlib import Path
import openpyxl
import pandas as df
from datetime import datetime

from order_extract import read_excel_lines, extract_item_lines,  extract_customer_lines, extract_header_lines
from order_parser import gen_parse_items, parse_header,parse_customer, parse_orders
from excel_export import orders_to_dataframe, export_to_excel_with_formatting, export_summary_statistics
from report import print_order_summary


def main():

    # 输入和输出目录
    raw_data_dir = Path(r"D:\PythonProjects\sales-order-parser\data\raw")
    processed_dir = Path(r"D:\PythonProjects\sales-order-parser\data\processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all orders and retrieve a list of orders data
    orders_data = parse_orders(raw_data_dir)
    if not orders_data:
        return

    # Print order summary
    print_order_summary(orders_data)
    
    # 转换为 DataFrame
    df = orders_to_dataframe(orders_data)

    # 显示数据预览
    print("\n📋 Data Preview (First 5 rows):")
    print("=" * 80)
    preview_cols = ['sales_order_no', 'customer_name', 'item_description', 'quantity', 'amount']
    print(df[preview_cols].head(5).to_string(index=0))
    
    # 导出详细数据到 Excel
    # output_file = processed_dir / f"all_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    # export_to_excel_with_formatting(df, output_file)
    # print(f"\n✅ Detailed orders exported to: {output_file}")
    
    # 导出统计摘要
    # export_summary_statistics(orders_data, processed_dir)
    

    
    # print(f"\n✅ Processing complete!")


        
if __name__ == "__main__":
    main()