from pathlib import Path
import openpyxl
import pandas as df
from datetime import datetime

from order_extract import read_excel_lines, extract_item_lines,  extract_customer_lines, extract_header_lines
from order_parser import gen_parse_items, parse_header,parse_customer, parse_orders
from excel_export import orders_to_dataframe, export_to_excel_with_formatting
from report import print_order_summary


def main():

    # 输入和输出目录
    # test data
    # raw_data_dir = Path(r"D:\PythonProjects\sales-order-parser\data\raw")
    # real data
    raw_data_dir = Path(r"D:\OC\OC20260813-Excel-Txt")
    processed_dir = Path(r"D:\PythonProjects\sales-order-parser\data\processed")
    processed_dir.mkdir(parents=True, exist_ok=True)


    # Process all orders and retrieve a list of orders data
    orders_data = parse_orders(raw_data_dir)
    if not orders_data:
        return

    # 转换为 DataFrame
    df = orders_to_dataframe(orders_data)
    
    # 导出详细数据到 Excel
    output_file = processed_dir / f"all_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    export_to_excel_with_formatting(df, output_file)
    print(f"\n✅ Detailed orders exported to: {output_file}")

        
if __name__ == "__main__":
    main()