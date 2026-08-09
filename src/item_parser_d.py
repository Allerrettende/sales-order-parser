import re

def extract_item(line):
    """
    从商品行中提取各个字段
    示例: "1.12.1.3.4 Product Name 999"
    """
    # 匹配商品行格式：版本号 + 描述 + 三位数字
    match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+?)\s+(\d{3})$', line)
    
    if not match:
        # 如果匹配失败，返回空的商品模板
        return {
            "pos_number": None,
            "item_description": None,
            "item_details": None,
            "quantity": None,
            "unit": None,
            "unit_price": None,
            "amount": None,
            "tax_code": None,
        }
    
    pos_number = match.group(1)  # 版本号: "1.12.1.3.4"
    description = match.group(2)  # 商品描述: "Product Name"
    amount = match.group(3)       # 金额: "999"
    
    # 这里可以进一步解析描述字段，提取数量、单位、单价等
    # 例如: "Product A 10 pcs @ 15.50" -> 数量=10, 单位=pcs, 单价=15.50
    
    # 简单版本：只提取基本字段
    return {
        "pos_number": pos_number,
        "item_description": description,
        "item_details": None,
        "quantity": None,
        "unit": None,
        "unit_price": None,
        "amount": amount,
        "tax_code": None,
    }


def extract_items(lines):
    """
    从文本行中提取商品信息
    每行可能是商品行或描述行
    """
    print("Extracting item information from lines...")
    
    current_item = None
    
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 检查是否为商品行
        match = re.match(r'^(\d+(?:\.\d+)*).*?\b(\d{3})$', line)
        
        if match:
            # 遇到新商品，先保存上一个
            if current_item:
                yield current_item
            
            # 开始新商品
            current_item = extract_item(line)
        else:
            # 描述行：追加到当前商品的详情
            if current_item:
                if current_item["item_details"]:
                    current_item["item_details"] += " " + line
                else:
                    current_item["item_details"] = line
            else:
                # 没有当前商品，忽略孤立的描述行
                print(f"Warning: Orphan description line ignored: {line}")
    
    # 返回最后一个商品
    if current_item:
        yield current_item


# ============ 增强版 extract_item（解析更多字段） ============

def extract_item_advanced(line):
    """
    增强版：尝试从商品行中提取更多字段
    支持格式: "1.0 Product Name 10 pcs @ 15.50 999"
    """
    match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+?)\s+(\d{3})$', line)
    if not match:
        return create_empty_item()
    
    pos_number = match.group(1)
    description_part = match.group(2)
    amount = match.group(3)
    
    # 尝试解析描述部分，提取数量、单位、单价
    # 模式: "描述 数量 单位 @ 单价"
    # 例如: "Product A 10 pcs @ 15.50"
    desc_match = re.match(r'^(.+?)\s+(\d+\.?\d*)\s+([a-zA-Z]+)\s+@\s+(\d+\.?\d*)$', description_part)
    
    if desc_match:
        item_description = desc_match.group(1)
        quantity = desc_match.group(2)
        unit = desc_match.group(3)
        unit_price = desc_match.group(4)
    else:
        # 简化：只提取描述
        item_description = description_part
        quantity = None
        unit = None
        unit_price = None
    
    return {
        "pos_number": pos_number,
        "item_description": item_description.strip(),
        "item_details": None,
        "quantity": quantity,
        "unit": unit,
        "unit_price": unit_price,
        "amount": amount,
        "tax_code": None,
    }


def create_empty_item():
    """创建空的商品模板"""
    return {
        "pos_number": None,
        "item_description": None,
        "item_details": None,
        "quantity": None,
        "unit": None,
        "unit_price": None,
        "amount": None,
        "tax_code": None,
    }


# ============ 使用示例 ============

if __name__ == "__main__":
    # 测试数据
    test_lines = [
        "1.12.1.3.4 Product A 999",
        "This is a detailed description of product A",
        "It has multiple lines of description",
        "2.0 Product B 10 pcs @ 15.50 500",
        "Product B details here",
        "3.0 Product C 200",
        "Final product details"
    ]
    
    print("=" * 50)
    print("Testing basic extractor:")
    print("=" * 50)
    
    # 使用基本版本
    for item in extract_items(test_lines):
        print(f"\nItem found:")
        for key, value in item.items():
            if value:
                print(f"  {key}: {value}")
    
    print("\n" + "=" * 50)
    print("Testing advanced extractor:")
    print("=" * 50)
    
    # 使用增强版（需要替换 extract_item）
    # 这里演示如何切换解析器
    def extract_items_advanced(lines):
        current_item = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(r'^(\d+(?:\.\d+)*).*?\b(\d{3})$', line)
            if match:
                if current_item:
                    yield current_item
                current_item = extract_item_advanced(line)
            else:
                if current_item:
                    if current_item["item_details"]:
                        current_item["item_details"] += " " + line
                    else:
                        current_item["item_details"] = line
        if current_item:
            yield current_item
    
    for item in extract_items_advanced(test_lines):
        print(f"\nItem found:")
        for key, value in item.items():
            if value:
                print(f"  {key}: {value}")