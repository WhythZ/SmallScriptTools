import os
import sys

# 文件路径、新文件名前缀、起始编号、处理的文件扩展名
def do_rename(path, prefix, start_number=1, file_extension=None):
    
    # 检查路径是否存在
    if not os.path.exists(path):
        print(f"ERROR: The path '{path}' does not exist")
        return False
    
    if not os.path.isdir(path):
        print(f"ERROR: The path '{path}' is not a folder")
        return False
    
    # 获取所有文件（排除目录）
    all_items = os.listdir(path)
    files = []
    
    for item in all_items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            # 如果指定了文件扩展名，进行筛选
            if file_extension:
                if item.lower().endswith(file_extension.lower()):
                    files.append(item)
            else:
                files.append(item)
    
    if not files:
        print("ERROR: No demanded files found to be renamed")
        return False
    
    # 按文件名排序
    files.sort()
    
    print(f"Found {len(files)} files:")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file}")
    print("Start renaming ...")

    # 计算需要的数字位数
    total_files = len(files)
    num_digits = len(str(start_number + total_files - 1))
    
    # 询问用户确认
    response = input(f"\nAre you sure to rename all files in '{prefix}0~' format? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled")
        return False
    
    # 执行重命名
    success_count = 0
    failed_files = []
    
    for i, old_name in enumerate(files, start_number):
        # 获取文件扩展名
        _, ext = os.path.splitext(old_name)
        
        # 生成新文件名
        number_str = str(i).zfill(num_digits)
        new_name = f"{prefix}{number_str}{ext}"
        
        old_path = os.path.join(path, old_name)
        new_path = os.path.join(path, new_name)
        
        try:
            # 检查新文件名是否已存在
            if os.path.exists(new_path):
                print(f"Warning: The new name '{new_name}' already exists, skipped renaming '{old_name}'")
                failed_files.append((old_name, "Target name already exists"))
                continue
            
            os.rename(old_path, new_path)
            print(f"Succeed to rename: '{old_name}' -> '{new_name}'")
            success_count += 1
            
        except Exception as e:
            print(f"Fail to rename: '{old_name}' -> {str(e)}")
            failed_files.append((old_name, str(e)))
    
    # 显示结果摘要
    print(f"\nRenaming completed")
    print(f"Success: {success_count}/{total_files}")

    if failed_files:
        print(f"Fail: {len(failed_files)}")
        for old_name, error in failed_files:
            print(f"  '{old_name}': {error}")
    return True

def main():
    # 获取用户输入
    path = input("Input the folder path of target files: ").strip()
    
    # 如果路径为空，使用当前目录
    if not path:
        path = "."
    
    prefix = input("Input the name prefix you want (such as 'btn_menu_'): ").strip()
    if not prefix:
        print("ERROR: The prefix cannot be empty")
        return
    
    # 询问起始编号
    start_input = input("Input the starting serial number (default as '1'): ").strip()
    if start_input:
        try:
            start_number = int(start_input)
        except ValueError:
            print("ERROR: Invalid number input")
            return
    else:
        start_number = 1
    
    # 询问文件类型筛选
    extension_input = input("Input the target filename extension (such as '.jpg'), input empty to handle all: ").strip()
    file_extension = None
    if extension_input:
        if not extension_input.startswith('.'):
            file_extension = '.' + extension_input
        else:
            file_extension = extension_input
    
    # 执行重命名
    do_rename(path, prefix, start_number, file_extension)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nProgram interrupted by error: {str(e)}")