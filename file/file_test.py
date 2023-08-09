import logging
import os

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


print(os.path.dirname("/home/chenbin/workspace/技术设计/GPT/metrics.json"))
print(os.path.basename("/home/chenbin/workspace/技术设计/GPT"))
