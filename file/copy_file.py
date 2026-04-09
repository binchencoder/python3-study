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


def copy_src(save_model_path, source_files):
    # 复制源码到save_model_path目录下
    logger.info(f"copy source code to {save_model_path}")

    for s in source_files:
        file_or_dir_name = os.path.basename(s)
        d = os.path.join(save_model_path, file_or_dir_name)
        logger.info(f"source: {s}, target: {d}")

        try:
            # 如果是文件夹，使用shutil.copytree
            if os.path.isdir(s):
                logger.info(f"copytree: {s} to {d}")
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                # 如果是文件，使用shutil.copy2
                logger.info(f"copy2: {s} to {d}")
                shutil.copy2(s, d)
        except Exception as e:
            logger.error(f"Error copying {s} to {d}: {e}")


def main():
    target_dir = "/home/chenbin/workspace/技术设计/test"
    try:
        source_files = [
            "/home/chenbin/workspace/技术设计/GPT/metrics.json",
            "/home/chenbin/workspace/技术设计/Labeling",
        ]
        copy_src(target_dir, source_files)
    except Exception as e:
        logger.info(f"copy source code to {target_dir} failed, {e}")
        # 断言
        assert False, f"copy source code to {target_dir} failed, {e}"


if __name__ == "__main__":
    main()
