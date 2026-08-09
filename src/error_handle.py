import re
import logging

# 配置日志
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def parse_item(line):
    """
    解析商品行，带完整的错误处理
    """
    if not line or not line.strip():
        logger.warning("Empty line provided to parse_item")
        return None
    
    parts = line.split()
    
    # 检查最小长度
    if len(parts) < 3:  # 至少要有编号、描述、金额
        logger.warning(f"Line has too few parts: {line}")
        return None
    
    try:
        # 使用正则表达式更精确地匹配
        match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+?)\s+(\d{3})$', line)
        if not match:
            logger.warning(f"Line doesn't match expected format: {line}")
            return None
        
        pos_number = match.group(1)
        description = match.group(2)
        amount = match.group(3)
        
        # 尝试提取额外字段（数量、单位、单价）
        quantity = None
        unit = None
        unit_price = None
        
        # 尝试匹配带数量单位的格式
        # 例如: "Product A 10 pcs @ 15.50"
        desc_match = re.match(r'^(.+?)\s+(\d+\.?\d*)\s+([a-zA-Z]+)\s+@\s+(\d+\.?\d*)$', description)
        if desc_match:
            description = desc_match.group(1)
            quantity = desc_match.group(2)
            unit = desc_match.group(3)
            unit_price = desc_match.group(4)
        
        return {
            "pos_number": pos_number,
            "item_description": description.strip(),
            "item_details": None,
            "quantity": quantity,
            "unit": unit,
            "unit_price": unit_price,
            "amount": amount,
            "tax_code": None,
        }
        
    except IndexError as e:
        logger.error(f"IndexError parsing line '{line}': {e}")
        return None
    except ValueError as e:
        logger.error(f"ValueError parsing line '{line}': {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error parsing line '{line}': {e}")
        return None


def extract_items(lines):
    """
    从文本行中提取商品信息，带错误处理
    """
    print("Extracting item information from lines...")
    current_item = None
    error_count = 0
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        # 检查是否为商品行
        match = re.match(r'^(\d+(?:\.\d+)*).*?\b(\d{3})$', line)
        
        if match:
            # 保存上一个商品
            if current_item:
                yield current_item
            
            # 解析新商品
            try:
                current_item = parse_item(line)
                if current_item is None:
                    # 解析失败，跳过
                    print(f"Warning: Failed to parse line {line_num}: {line}")
                    error_count += 1
                    current_item = None
                    continue
            except Exception as e:
                print(f"Error parsing line {line_num}: {line}")
                print(f"Error: {e}")
                error_count += 1
                current_item = None
                continue
        else:
            # 描述行
            if current_item:
                if current_item.get("item_details"):
                    current_item["item_details"] += " " + line
                else:
                    current_item["item_details"] = line
            else:
                # 孤立的描述行
                print(f"Warning: Orphan description line {line_num}: {line}")
    
    # 返回最后一个商品
    if current_item:
        yield current_item
    
    # 统计信息
    if error_count > 0:
        print(f"Processing completed with {error_count} errors")


# 使用示例
if __name__ == "__main__":
    test_lines = [
        "1.12.1.3.4 Product A 999",
        "This is a detailed description",
        "2.0 Product B 10 pcs @ 15.50 500",
        "INVALID LINE",  # 这行会导致错误
        "3.0 Product C 200",
        "Product C details"
    ]
    
    for item in extract_items(test_lines):
        if item:
            print(f"\nItem found:")
            for key, value in item.items():
                if value:
                    print(f"  {key}: {value}")