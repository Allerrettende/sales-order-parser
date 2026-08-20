import pandas as pd
from pathlib import Path
from order_parser import parse_orders
from excel_process import  append_multiple_orders, append_new_orders_from_b_to_a
from order_dataframe import orders_to_dataframe

def append_daily():

    # 输入和输出目录
    # test data
    # raw_data_dir = Path(r"D:\PythonProjects\sales-order-parser\data\raw")

    # real data
    raw_data_dir = Path(r"D:\OC Extract")
    # raw_data_dir = Path(r"D:\OC\Test")
    current_excel_path = Path(r"D:\OC\oc_temp.xlsx")
  
    new_orders = parse_orders(raw_data_dir)
    if not new_orders:
        print("No files found")
        return

    # 转换为 DataFrame
    df = orders_to_dataframe (new_orders)
    
    # 安全追加（带去重）
    append_multiple_orders(df, current_excel_path)


# 每天运行一次，从中间表导入新订单到主表

def daily_import():
    """
    每日导入新订单
    """
    main_file = r'D:\OC\OC Master List.xlsx'      # A文件：主表（已格式化）
    temp_file = r'D:\OC\oc_temp.xlsx'        # B文件：中间表（新订单）
    
    success = append_new_orders_from_b_to_a(
        main_file=main_file,
        temp_file=temp_file,
        sheet_name='Orders',
        order_column='sales_order_no'
    )
    
    if success:
        print("🎉 Daily import completed!")
        
        # 可选：清空中间文件或移动到归档
        # backup_temp_file(temp_file)
    else:
        print("❌ Daily import failed, please check logs")



if __name__ == "__main__":

    # append_daily()
    
    daily_import()
