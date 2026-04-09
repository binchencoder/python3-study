import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def test_str_date():
    now = datetime.now()
    return now.strftime("%Y%m%d")


if __name__ == '__main__':
    logger.info(f"str(date) = {test_str_date()}")
