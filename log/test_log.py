import logging

# 设置日志
logging.basicConfig(
    filename="./test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("this is log")
