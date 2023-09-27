import logging
import os
import shutil

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

dir = "/Users/binchen/Download/Test"

os.makedirs(dir)

# 递归删除非空目录
shutil.rmtree(dir)


"""
https://geek-docs.com/python/python-file-tutorials/181_python_delete_folder.html

"""
