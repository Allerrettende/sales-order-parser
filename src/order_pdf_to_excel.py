import subprocess
import pandas as pd
from pathlib import Path
import tempfile
import re

def clean_for_excel(text):
    """
    清理 Excel 不支持的特殊字符
    """
    if not text:
        return text
    
    # Excel 不支持的控制字符，移除所有控制字符（除了换行符和制表符），使用正则表达式移除控制字符。 保留换行符 (\n) 和制表符 (\t)
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return cleaned

def extract_with_poppler(pdf_path, poppler_path):
    """
    使用 Poppler 的 pdftotext 提取文本
    """
    # 创建临时文本文件
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+', encoding='utf-8') as tmp:
        txt_path = tmp.name
    try:
        # 使用 -q 参数静默模式，只显示严重错误。 -layout 保留原来布局。
        cmd = [poppler_path, '-layout', '-q', str(pdf_path), txt_path]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # 读取提取的文本
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 按行分割
        lines = text.split('\n')
        return lines
        
    finally:
        # 清理临时文件
        Path(txt_path).unlink(missing_ok=True)

def find_poppler():
    # 查找 Poppler 的 pdftotext.exe
    possible_paths = [
        r"P:\PM\Project List\Tools\poppler\bin\pdftotext.exe",
        r"D:\Tools\poppler\bin\pdftotext.exe",
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            return path
    return None

def export_single_pdf(pdf_path, output_folder, poppler_path):
  
    file_name = pdf_path.stem
    # 提取原始行数据
    lines = extract_with_poppler(pdf_path, poppler_path)
    if not lines:
        print(f"  ⚠️  没有提取到数据")
        return 0

    # 1. 导出为TXT（保留原始样貌）
    txt_file = output_folder / f"{file_name}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

    # 2. 导出为Excel（清理特殊字符）
    excel_file = output_folder / f"{file_name}.xlsx"
    
    # 清理每一行的特殊字符，列表推导式。
    cleaned_lines = [clean_for_excel(line) if line else '' for line in lines]
    
    # 创建DataFrame
    df = pd.DataFrame(cleaned_lines)
    df.to_excel(excel_file, index=False, header=False, engine='openpyxl')
  
    return len(lines)

def batch_export(input_folder, output_folder):

    # 查找 Poppler
    poppler_path = find_poppler()
    if not poppler_path:
        print("未找到 Poppler，请检查路径")
        return
    
    # 获取所有PDF文件
    pdf_files = list(Path(input_folder).glob('*.pdf'))
    
    if not pdf_files:
        print("没有找到PDF文件")
        return
    
    # 创建输出目录
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_lines = 0
    
    for pdf_file in pdf_files:
        try:
            # print(f"处理: {pdf_file.name}")
            line_count = export_single_pdf(pdf_file, output_path, poppler_path)
            if line_count > 0:
                total_lines += line_count
                success_count += 1
            else:
                print(f"无数据")
        except Exception as e:
            print(f"错误: {e}")
    
    print(f"📊 完成: 成功 {success_count}/{len(pdf_files)} 个文件")
    print(f"📊 总行数: {total_lines}")
    print(f"📁 输出位置: {output_path}")


if __name__ == "__main__":

    input_folder = r"D:\OC\OC 2014-20260818-PDF"
    output_folder = r"D:\OC\OC 2014-20260818-Excel"
    
    batch_export(input_folder, output_folder)