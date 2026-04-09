import zipfile


def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)


# 测试函数
if __name__ == "__main__":
    unzip_file("/home/chenbin/data/whisper.zip", "/home/chenbin/data")
