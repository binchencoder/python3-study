import json
import os
import logging
from obs import ObsClient
import requests
from typing import Optional
import argparse
import zipfile

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def progress_callback_factory():
    last_reported = [0]  # 非局部变量，保存上一次报告的进度

    def progress_callback(transferred, _current_chunk_size, total):
        """
        回调函数，计算下载的百分比。

        :param transferred: 已传输的数据量
        :param _current_chunk_size: 当前分块的数据量，忽略
        :param total: 文件的总大小
        """
        nonlocal last_reported
        if total == 0:  # 避免除以零的错误
            logger.warning("Total file size reported as 0. Skipping progress update.")
            return
        progress = (transferred / total) * 100
        if progress - last_reported[0] >= 1:  # 只有当进度增加了1%时才报告
            last_reported[0] = progress
            logger.info(
                f"Downloaded {transferred} out of {total} bytes ({progress:.2f}%)"
            )
            # print(f"Downloaded {transferred} out of {total} bytes ({progress:.2f}%)")

    return progress_callback


def download_from_obs(obs_client, bucket_name, obs_key, local_directory):
    # 获取OBS中的所有对象
    keys = []
    resp = obs_client.listObjects(bucket_name, prefix=obs_key)
    print(json.dumps(resp))
    while resp.is_truncated:
        keys += [content.key for content in resp.body.contents]
        resp = obs_client.listObjects(
            bucket_name, prefix=obs_key, marker=resp.body.next_marker
        )
    keys += [content.key for content in resp.body.contents]

    for key in keys:
        file_name = key[len(obs_key) :]
        if len(file_name) == 0:
            file_name = os.path.basename(obs_key).split("/")[-1]
        local_file_path = os.path.join(local_directory, file_name)
        if key.endswith("/"):  # 如果是目录
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            continue
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))
        logger.info(f"Starting to download file {key}")
        obs_client.downloadFile(
            bucket_name,
            key,
            local_file_path,
            progressCallback=progress_callback_factory(),
        )
        logger.info(f"File {key} downloaded successfully to {local_file_path}")


def download_directory_from_obs(
    s3_path: str,
    obs_access_key: str,
    obs_secret_key: str,
    local_directory: str,
    endpoint_url: Optional[str] = None,
) -> bool:
    """
    从OBS下载目录中的所有文件到本地

    :param obs_access_key: OBS的access key
    :param obs_secret_key: OBS的secret key
    :param s3_path: 远程目录路径（在OBS中的位置）或OBS URL
    :param local_directory: 本地目录路径（文件将被下载到哪里）
    :param endpoint_url: OBS服务的endpoint url
    :return: 若下载成功返回True，否则返回False
    """
    try:
        # 判断是否为OBS URL
        if s3_path.startswith("s3://"):
            path_parts = s3_path[5:].split("/")
            bucket_name = path_parts[0]
            s3_path = "/".join(path_parts[1:])
        obs_client = ObsClient(
            access_key_id=obs_access_key,
            secret_access_key=obs_secret_key,
            server=endpoint_url,
        )

        # obs_client.uploadFile(bucketName=bucket_name, objectKey=)

        download_from_obs(obs_client, bucket_name, s3_path, local_directory)
        if s3_path.endswith(".zip"):
            file_path = local_directory + "/" + s3_path.split("/")[-1]
            logger.info(f"===zip file path is {file_path}====")

            with zipfile.ZipFile(f"{file_path}", "r") as zip_ref:
                zip_ref.extractall(f"{local_directory}")

            if os.path.exists(f"{file_path}"):
                os.remove(f"{file_path}")

        return True

    except Exception as e:
        logger.error(f"Error while downloading directory from OBS: {e}")
        return False


# 测试函数
if __name__ == "__main__":
    download_directory_from_obs(
        "s3://pie-engine-gpt/demo/ohmyzsh-master.zip",
        "3C0JZGAMQNDW4V79AFNM",
        "dC3JVwrefYyeBvRDnIS8XketdopCQW80E8wpJs9K",
        "/home/chenbin",
        "https://obs.cn-north-4.myhuaweicloud.com",
    )

    # 参数解析
    # parser = argparse.ArgumentParser(description='Download directory from OBS.')
    # parser.add_argument('--s3_path', required=True, help='Path to the OBS directory.')
    # parser.add_argument('--obs_access_key', required=True, help='OBS access key.')
    # parser.add_argument('--obs_secret_key', required=True, help='OBS secret key.')
    # parser.add_argument('--local_directory', required=True, help='Local directory to download the files.')
    # parser.add_argument('--endpoint_url', default=None, help='Endpoint URL of the OBS service.')

    # args = parser.parse_args()
    # # 在一行中打印出传入的参数和每一个参数名
    # logger.info(f"传入参数: {', '.join(f'{k}={v}' for k, v in vars(args).items())}")

    # result = download_directory_from_obs(
    #     args.s3_path, args.obs_access_key, args.obs_secret_key, args.local_directory, args.endpoint_url)
    # assert result, "Directory download failed"
    # 参数解析
    # parser = argparse.ArgumentParser(description='Download files from OBS and HTTP.')
    # parser.add_argument('--s3_path', nargs='+', required=True, help='List of paths to the OBS or HTTP files.')
    # parser.add_argument('--obs_access_key', required=True, help='OBS access key.')
    # parser.add_argument('--obs_secret_key', required=True, help='OBS secret key.')
    # parser.add_argument('--local_directory', required=True, help='Local directory to download the files.')
    # parser.add_argument('--endpoint_url', default=None, help='Endpoint URL of the OBS service.')

    # args = parser.parse_args()

    # 在一行中打印出传入的参数和每一个参数名
    # logger.info(f"传入参数: {', '.join(f'{k}={v}' for k, v in vars(args).items())}")

    # result = download_files_from_links(
    #    args.s3_path, args.obs_access_key, args.obs_secret_key, args.local_directory, args.endpoint_url)
    # assert result, "Files download failed"

# python s3_data_downloader.py --s3_path "s3://pie-engine-gpt/knowledge/models/578529101478141952" --obs_access_key "3C0JZGAMQNDW4V79AFNM" --obs_secret_key "dC3JVwrefYyeBvRDnIS8XketdopCQW80E8wpJs9K" --local_directory "./download" --endpoint_url "obs.cn-north-4.myhuaweicloud.com"
# python s3_data_downloader.py --s3_path "https://www.baidu.com" "s3://pie-engine-gpt/knowledge/models/578529101478141952" --obs_access_key "3C0JZGAMQNDW4V79AFNM" --obs_secret_key "dC3JVwrefYyeBvRDnIS8XketdopCQW80E8wpJs9K" --local_directory "./download" --endpoint_url "obs.cn-north-4.myhuaweicloud.com"
