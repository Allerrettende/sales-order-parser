import os
import shutil
from pathlib import Path
from datetime import datetime

'''
路径结构说明
程序会扫描以下路径：

P:\PM\AHK\Order Confirmation

P:\PM\BOS\Order Confirmation

P:\PM\其他项目\Order Confirmation

所有以 "O" 开头的 PDF 文件都会复制到 D:\Back\OC，不保留目录结构。

清晰结构: 每个项目下一层就是 Order Confirmation 目录

高效扫描: 直接检查每个项目下是否存在 Order Confirmation 目录
'''

def backup_pdf_files():
    """
    备份所有 Order Confirmation 目录下以 'O' 开头的 PDF 文件
    源路径结构: P:\PM\{项目名}\Order Confirmation
    目标路径: D:\Back\OC
    """
    # 配置路径
    base_source = r"P:\PM"
    target_root = r"D:\Back\OC"
    
    source_path = Path(base_source)
    target_path = Path(target_root)
    
    # 检查源目录是否存在
    if not source_path.exists():
        print(f"❌ 错误: 源目录不存在 - {source_path}")
        return
    
    # 创建目标目录
    try:
        target_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ 目标目录已准备: {target_path}")
    except Exception as e:
        print(f"❌ 创建目标目录失败: {e}")
        return
    
    print("="*70)
    print(f"开始扫描: {source_path}")
    print(f"目标目录: {target_path}")
    print("="*70)
    
    # 统计信息
    total_files = 0
    copied_files = 0
    skipped_files = 0
    error_files = 0
    processed_folders = 0
    found_projects = 0
    
    # 遍历 PM 下的所有项目目录（AHK、BOS等）
    for project_dir in source_path.iterdir():
        if not project_dir.is_dir():
            continue
        
        found_projects += 1
        print(f"\n📂 扫描项目: {project_dir.name}")
        
        # 构建 Order Confirmation 路径: P:\PM\项目名\Order Confirmation
        oc_path = project_dir / "Order Confirmation"
        
        if not oc_path.exists() or not oc_path.is_dir():
            print(f"  ℹ️  项目 {project_dir.name} 中没有 Order Confirmation 目录")
            continue
        
        processed_folders += 1
        print(f"\n  📁 [{processed_folders}] {oc_path}")
        
        # 查找所有以 'O' 开头的 PDF 文件
        try:
            # 获取目录中所有以 'O' 开头的 .pdf 文件（不区分大小写）
            pdf_files = [f for f in oc_path.iterdir() 
                       if f.is_file() 
                       and f.name.lower().startswith('o') 
                       and f.suffix.lower() == '.pdf']
            
            if not pdf_files:
                print(f"    ℹ️  没有找到以 'O' 开头的 PDF 文件")
                continue
            
            print(f"    📄 找到 {len(pdf_files)} 个 PDF 文件")
            
            for pdf_file in pdf_files:
                total_files += 1
                
                # 目标文件路径（直接放在 OC 目录下）
                dest_file = target_path / pdf_file.name
                
                # 检查文件是否已存在
                if dest_file.exists():
                    # 如果文件名相同，检查是否内容相同
                    try:
                        if dest_file.stat().st_size == pdf_file.stat().st_size:
                            print(f"    ⏭️  跳过: {pdf_file.name} (已存在且大小相同)")
                            skipped_files += 1
                            continue
                        else:
                            # 文件名相同但大小不同，添加时间戳
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            new_name = f"{pdf_file.stem}_{timestamp}{pdf_file.suffix}"
                            dest_file = target_path / new_name
                            print(f"    📝  重命名: {pdf_file.name} -> {new_name}")
                    except Exception as e:
                        print(f"    ⚠️  检查文件时出错: {e}")
                
                # 复制文件
                try:
                    shutil.copy2(pdf_file, dest_file)
                    copied_files += 1
                    size = pdf_file.stat().st_size
                    size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
                    print(f"    ✅ 复制: {pdf_file.name} ({size_str})")
                except Exception as e:
                    error_files += 1
                    print(f"    ❌ 复制失败: {pdf_file.name} - {e}")
                    
        except PermissionError as e:
            print(f"    ❌ 权限错误: {e}")
        except Exception as e:
            print(f"    ❌ 处理目录失败: {e}")
    
    # 输出统计信息
    print("\n" + "="*70)
    print("📊 备份完成统计:")
    print(f"  - 扫描的项目数: {found_projects}")
    print(f"  - 找到的 Order Confirmation 目录数: {processed_folders}")
    print(f"  - 找到的文件总数: {total_files}")
    print(f"  - 成功复制: {copied_files}")
    print(f"  - 跳过文件: {skipped_files}")
    print(f"  - 失败文件: {error_files}")
    print(f"  - 目标位置: {target_path}")
    print("="*70)

if __name__ == "__main__":
    backup_pdf_files()