from pathlib import Path
import pandas as df

from order_parser import  parse_orders
from excel_process import  export_to_excel_with_formatting
from order_dataframe import orders_to_dataframe
from report import print_order_summary

def main():

    # 输入和输出目录
    # test data
    # raw_data_dir = Path(r"D:\PythonProjects\sales-order-parser\data\raw")

    # real data
    raw_data_dir = Path(r"D:\OC\OC 2014-20260818-Excel")
    raw_data_dir = Path(r"D:\OC\Test")
    processed_dir = Path(r"D:\OC")
    processed_dir.mkdir(parents=True, exist_ok=True)

    orders_data = parse_orders(raw_data_dir)
    if not orders_data:
        print("No files found")
        return

    # 转换为 DataFrame
    df = orders_to_dataframe(orders_data)
    
    # 导出详细数据到 Excel

    output_file = processed_dir / f"all_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    export_to_excel_with_formatting(df, output_file)
    print(f"\n✅ Detailed orders exported to: {output_file}")

        
if __name__ == "__main__":
    main()