import os

if __name__ == "__main__":
    # 指定文件夹路径
    folder_path = "/home/chenbin/data"
    # 使用os.listdir()列出文件夹中的所有文件
    files = os.listdir(folder_path)

    # 输出所有文件名
    for file in files:
        print(file)

    # 使用os.scandir()函数列出文件夹中的所有文件
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file():
                print(entry.path)

    os.makedirs("/outputs/123123")
