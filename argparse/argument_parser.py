import argparse
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

excluded_args = [
    "s3_path",
    "obs_access_key",
    "obs_secret_key",
]


def main():
    parser = argparse.ArgumentParser(description="Test argument parser")
    parser.add_argument("--dataset_path", required=True, help="")
    parser.add_argument("--test_dataset_path", required=False, help="")

    args, unknown_args = parser.parse_known_args()  # 使用parse_known_args代替parse_args

    logger.info(f"args:: {args}")

    args_dict = vars(args)
    for key, value in args_dict.items():
        if key not in excluded_args:  # 不在排除列表中
            if key == "test_dataset_path" and (value is None or not value.strip()):
                continue
            logger.info(f"key: {key}, value: {value}")


if __name__ == "__main__":
    main()
