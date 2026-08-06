import re
from pathlib import Path
from extract_order_excel import read_excel_lines


def extract_item_lines(lines):
    """
    提取产品行，包括主行和描述行
    """
    item_lines = []
    collecting = False
    
    # 开始标记
    start_pattern = re.compile(r'^Pos\.\s+Item\s+Description', re.IGNORECASE)
    
    # 结束标记
    end_patterns = [
        re.compile(r'Subtotal\s+RMB', re.IGNORECASE),
        re.compile(r'^_x000C_', re.IGNORECASE),
        re.compile(r'Page\s+\d+', re.IGNORECASE),
        re.compile(r'Agreed payment', re.IGNORECASE),
    ]
    
    # 需要排除的行模式
    exclude_patterns = [
        re.compile(r'^Balance\s+'),
        re.compile(r'^Subtotal\s+'),
        re.compile(r'^Total\s+'),
        re.compile(r'^Page\s+'),
        re.compile(r'_x000C_'),
        re.compile(r'^Pos\.\s+Item\s+Number\.Item\s+Description', re.IGNORECASE),
        re.compile(r'^Item\s+Number\.Item\s+Description', re.IGNORECASE),
        re.compile(r'^Pos\.\s+Item\s+Number\s+Item\s+Description', re.IGNORECASE),
        re.compile(r'Lieferdatum', re.IGNORECASE),
        re.compile(r'plus VAT', re.IGNORECASE),
        re.compile(r'^\s*[\d\.,]+\s*$'),
    ]
    
    # 产品行判断：包含数量、单位、单价、金额、税码
    product_pattern = re.compile(
        r'\d+,\d{2}\s+'
        r'[A-Za-z]+\s+'
        r'[\d\.]+,\d{2}\s+'
        r'[\d\.]+,\d{2}\s+'
        r'\d{3}'
    )
    
    # group行模式
    group_pattern = re.compile(r'^\d+\s+-.*-\s*$')
    
    for line_num, line in enumerate(lines, 1):
        line_stripped = line.strip()
        
        if not line_stripped:
            continue
        
        if start_pattern.search(line_stripped):
            print(f"✅ 找到开始标记在第 {line_num} 行")
            collecting = True
            continue
        
        if not collecting:
            continue
        
        should_end = False
        for pattern in end_patterns:
            if pattern.search(line_stripped):
                print(f"✅ 找到结束标记在第 {line_num} 行")
                should_end = True
                break
        if should_end:
            break
        
        if group_pattern.match(line_stripped):
            continue
        
        should_exclude = False
        for pattern in exclude_patterns:
            if pattern.search(line_stripped) or pattern.match(line_stripped):
                should_exclude = True
                break
        if should_exclude:
            continue
        
        is_product = product_pattern.search(line_stripped)
        
        if is_product:
            item_lines.append(line_stripped)
        else:
            if not re.match(r'^\d+', line_stripped) or line_stripped.startswith(' '):
                item_lines.append(line_stripped)
    
    return item_lines


def parse_product_line(line):
    """
    解析产品主行，提取各个字段
    
    示例输入:
    "1        Windows 11 GGWA                                                                  1,00 piece                  1.700,00               1.700,00 903"
    
    返回:
    {
        'pos': '1',
        'description': 'Windows 11 GGWA',
        'quantity': 1.00,
        'unit': 'piece',
        'unit_price': 1700.00,
        'total_price': 1700.00,
        'tc': '903'
    }
    """
    line_stripped = line.strip()
    
    # 方法1: 从右向左解析（更可靠）
    # 格式: ... [Quantity] [Unit] [Unit Price] [Total Price] [TC]
    # 数量: 1,00 或 1.00
    # 单位: piece, Piece, 等
    # 单价: 1.700,00
    # 总价: 1.700,00
    # 税码: 903 (3位数字)
    
    # 从右边开始匹配
    # 匹配模式: 数量 + 单位 + 单价 + 总价 + 税码
    right_pattern = re.compile(
        r'(\d+,\d{2})\s+'          # Quantity: 1,00
        r'([A-Za-z]+)\s+'          # Unit: piece
        r'([\d\.]+,\d{2})\s+'      # Unit Price: 1.700,00
        r'([\d\.]+,\d{2})\s+'      # Total Price: 1.700,00
        r'(\d{3})$'                # TC: 903 (到行尾)
    )
    
    match = right_pattern.search(line_stripped)
    if not match:
        return None
    
    quantity, unit, unit_price, total_price, tc = match.groups()
    
    # 获取数量开始的位置，之前的都是描述
    desc_end_pos = match.start()
    description = line_stripped[:desc_end_pos].strip()
    
    # 提取Pos号（行首的数字）
    pos_match = re.match(r'^(\d+(?:\.\d+)?)\s+', description)
    if pos_match:
        pos = pos_match.group(1)
        # 从描述中移除Pos号
        description = description[pos_match.end():].strip()
    else:
        pos = ''
    
    # 清理描述（去除多余空格）
    description = ' '.join(description.split())
    
    # 转换数字
    def parse_german_number(num_str):
        try:
            return float(num_str.replace('.', '').replace(',', '.'))
        except:
            return 0.0
    
    return {
        'pos': pos,
        'description': description,
        'quantity': parse_german_number(quantity),
        'unit': unit,
        'unit_price': parse_german_number(unit_price),
        'total_price': parse_german_number(total_price),
        'tc': tc
    }


def parse_order_items(lines):
    """
    解析订单中的所有产品行和描述行，组合成完整的产品数据
    """
    # 首先提取所有行
    raw_lines = extract_item_lines(lines)
    
    items = []
    current_item = None
    
    # 产品行判断模式
    product_pattern = re.compile(
        r'\d+,\d{2}\s+'
        r'[A-Za-z]+\s+'
        r'[\d\.]+,\d{2}\s+'
        r'[\d\.]+,\d{2}\s+'
        r'\d{3}'
    )
    
    for line in raw_lines:
        line_stripped = line.strip()
        
        # 检查是否是产品主行
        is_product = product_pattern.search(line_stripped)
        
        if is_product:
            # 保存上一个产品
            if current_item:
                items.append(current_item)
            
            # 解析新产品
            parsed = parse_product_line(line_stripped)
            if parsed:
                current_item = parsed
                current_item['details'] = []  # 用于存储描述行
                print(f"📦 解析产品: {parsed['pos']} - {parsed['description']}")
        else:
            # 描述行
            if current_item is not None:
                current_item['details'].append(line_stripped)
                print(f"📝 添加描述: {line_stripped[:50]}...")
    
    # 添加最后一个产品
    if current_item:
        items.append(current_item)
    
    return items


def print_items(items):
    """
    打印解析后的产品数据
    """
    print("\n" + "="*80)
    print("解析结果:")
    print("="*80)
    
    for i, item in enumerate(items, 1):
        print(f"\n产品 {i}:")
        print(f"  Pos No:        {item['pos']}")
        print(f"  Description:   {item['description']}")
        print(f"  Quantity:      {item['quantity']:.2f} {item['unit']}")
        print(f"  Unit Price:    {item['unit_price']:,.2f}")
        print(f"  Total Price:   {item['total_price']:,.2f}")
        print(f"  TC:            {item['tc']}")
        
        if item['details']:
            print(f"  Details:")
            for detail in item['details']:
                print(f"    - {detail}")
    
    print("\n" + "="*80)
    print(f"共解析了 {len(items)} 个产品")
    print("="*80)


def export_to_dict(items):
    """
    将产品数据导出为字典列表（每个产品包含Pos字段）
    """
    result = []
    for item in items:
        product_dict = {
            'Pos': item['pos'],
            'description': item['description'],
            'quantity': item['quantity'],
            'unit': item['unit'],
            'unit_price': item['unit_price'],
            'total_price': item['total_price'],
            'tc': item['tc'],
            'details': item['details']
        }
        result.append(product_dict)
    return result


def print_items(items):
    """
    打印解析后的产品数据
    """
    print("\n" + "="*80)
    print("解析结果:")
    print("="*80)
    
    for i, item in enumerate(items, 1):
        print(f"\n产品 {i}:")
        print(f"  Pos No:        {item['pos']}")
        print(f"  Description:   {item['description']}")
        print(f"  Quantity:      {item['quantity']:.2f} {item['unit']}")
        print(f"  Unit Price:    {item['unit_price']:,.2f}")
        print(f"  Total Price:   {item['total_price']:,.2f}")
        print(f"  TC:            {item['tc']}")
        
        if item['details']:
            print(f"  Details:")
            for detail in item['details']:
                print(f"    - {detail}")
    
    print("\n" + "="*80)
    print(f"共解析了 {len(items)} 个产品")
    print("="*80)


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # 测试两个文件
    files = [
        BASE_DIR / "data" / "raw" / "Order Confirmation 2025-864059.xlsx",
        BASE_DIR / "data" / "raw" / "Order Confirmation 2026-864117.xlsx"
    ]
    
    for file in files:
        if not file.exists():
            continue
            
        print("\n" + "="*80)
        print(f"处理文件: {file.name}")
        print("="*80)
        
        result = read_excel_lines(file)
        all_line = result["all_lines"]
        
        print(f"从Excel读取了 {len(all_line)} 行")
        print("\n开始解析订单...")
        print("-"*80)
        
        # 解析订单
        items = parse_order_items(all_line)
        
        # 打印结果
        print_items(items)
        
        # 导出为字典列表
        items_dict = export_to_dict(items)
        print("\n字典格式:")
        for product in items_dict:
            print(product)
        
        # 或者以更清晰的格式打印
        print("\n清晰的字典格式:")
        import json
        print(json.dumps(items_dict, indent=2, ensure_ascii=False))