import os

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

    # 计算需要的数字位数
    total_files = len(files)
    num_digits = len(str(start_number + total_files - 1))
    
    # 询问用户确认
    example_number = str(start_number).zfill(num_digits)
    response = input(f"Are you sure to rename all files in format like '{prefix}{example_number}'? (y/n): ")
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
                failed_files.append((old_name, "Target name already exists"))
                continue
            os.rename(old_path, new_path)
            success_count += 1
        except Exception as e:
            failed_files.append((old_name, str(e)))
    
    # 显示结果摘要
    print(f"Renaming completed {success_count}/{total_files}")

    if failed_files:
        for old_name, error in failed_files:
            print(f"Failed to rename '{old_name}': {error}")
    return True

def do_prepare():
    # 若输入路径为空则使用当前目录
    path = input("Input the absolute path of target files (default to use current): ").strip()
    if not path:
        path = "."
    
    # 询问重命名后的名称前缀
    prefix = input("Input the name prefix you want (such as 'btn_menu_'): ").strip()
    if not prefix:
        print("ERROR: The prefix cannot be empty")
        return
    
    # 询问起始编号
    start_input = input("Input the starting serial number (default to use '1'): ").strip()
    if start_input:
        try:
            start_number = int(start_input)
        except ValueError:
            print("ERROR: Invalid number input")
            return
    else:
        start_number = 1
    
    # 询问文件类型筛选
    file_extension = None
    # extension_input = input("Input the target file extension (default to handle all): ").strip()
    # if extension_input:
    #     if not extension_input.startswith('.'):
    #         file_extension = '.' + extension_input
    #     else:
    #         file_extension = extension_input
    
    # 执行重命名
    do_rename(path, prefix, start_number, file_extension)

if __name__ == "__main__":
    try:
        # 重复执行，直到用户Ctrl+C退出
        while True:
            do_prepare()
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"Program interrupted by error: {str(e)}")