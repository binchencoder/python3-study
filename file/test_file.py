def read_file(filepath: str) -> str:
    # 检查文件是否存在
    try:
        # 如果文件存在，以只读模式打开并读取内容
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
            print(f"文件 '{filepath}' 已存在，正在读取内容...")
            return file_content
    except FileNotFoundError as ffe:
        print(f"发生错误: {ffe}")
    except Exception as e:
        # 捕获其他可能的异常（如权限问题等）
        print(f"发生错误: {e}")
        return ""


def write_file(filepath: str, content: str = None) -> str:
    """
    如果文件存在，则读取其内容并返回。
    如果文件不存在，则先创建文件，并写入指定内容，然后返回写入的内容。

    参数:
        filepath (str): 文件的路径。
        content (str): 如果文件不存在，要写入的新内容。

    返回:
        str: 文件内容。
    """
    # 检查文件是否存在
    try:
        # 如果文件存在，以只读模式打开并读取内容
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
            print(f"文件 '{filepath}' 已存在，正在读取内容...")
            return file_content
    except FileNotFoundError:
        # 如果文件不存在，以写入模式创建文件并写入内容
        print(f"文件 '{filepath}' 不存在，正在创建并写入内容...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        # 写入完成后，再次以只读模式打开并返回内容，以确保返回的是磁盘上的实际内容
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        # 捕获其他可能的异常（如权限问题等）
        print(f"发生错误: {e}")
        return ""


if __name__ == "__main__":
    # 示例1: 文件不存在，将创建并写入内容
    file_path_1 = "example_new_file.txt"
    new_content = "这是新创建的文件内容。\nHello, World!"

    print("--- 首次调用：文件不存在 ---")
    file_content_1 = read_file(file_path_1)
    print(f"返回的内容是：\n'{file_content_1}'\n")

    # 示例2: 文件已存在，将直接读取内容
    print("--- 再次调用：文件已存在 ---")
    file_content_2 = write_file(file_path_1, "这个内容将不会被写入。")
    print(f"返回的内容是：\n'{file_content_2}'\n")

    # 示例3: 处理多级目录
    import os

    os.makedirs("data/files", exist_ok=True)  # 确保目录存在
    file_path_3 = "data/files/another_file.txt"

    print("--- 首次调用：处理多级目录 ---")
    file_content_3 = write_file(file_path_3, "这是一个在子目录中的文件。")
    print(f"返回的内容是：\n'{file_content_3}'\n")
