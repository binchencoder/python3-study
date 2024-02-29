import logging
import os
import shutil
import stat

"""
https://geek-docs.com/python/python-file-tutorials/181_python_delete_folder.html

"""

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# dir = "/Users/binchen/Download/Test"

# os.makedirs(dir)

# 递归删除非空目录
# shutil.rmtree(dir)


def remove_dir(dir_path):
    try:
        os.rmdir(dir_path)
    except OSError as e:
        print("目录删除失败:", e)


def remove_directory(directory):
    try:
        shutil.rmtree(directory)
        print("目录删除成功")
    except OSError as e:
        print("目录删除失败：", e)


def file_remove_readonly(func, path, execinfo):
    os.chmod(path, stat.S_IWUSR)  # 修改文件权限
    func(path)


def remove_directory_file(path):
    """
    remove files in directory
    """
    for itr_file in os.scandir(path):
        file_path = os.path.join(path, itr_file.path)
        logger.info(f"deleted:{file_path}")
        if itr_file.is_file():
            if not os.access(itr_file, os.W_OK):
                os.chmod(itr_file, stat.S_IWUSR)
            os.remove(itr_file)
        else:
            shutil.rmtree(itr_file, onerror=file_remove_readonly)


if __name__ == "__main__":
    # remove_dir("/home/chenbin/data/111/")
    remove_directory("/home/chenbin/data/111/")
