import boto3
from botocore.exceptions import ClientError


def init_s3_client(endpoint_url, s3_access_key, s3_secret_key):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
        # region_name='cn-north-1',  # 中国区域示例
        endpoint_url=endpoint_url,
    )
    return s3_client


def generate_signed_url(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    endpoint_url: str,
    bucket_name: str,
    object_key: str,
):
    s3 = init_s3_client(
        endpoint_url=endpoint_url,
        s3_access_key=aws_access_key_id,
        s3_secret_key=aws_secret_access_key,
    )

    try:
        # 设置URL有效期（单位：秒）
        url_expiration = 60 * 1000

        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=url_expiration,
        )

        return response
    except ClientError as e:
        print("Failed to generate signed URL for %s/%s" % (bucket_name, object_key))
        raise e


# 测试函数
if __name__ == "__main__":

    # 调用示例
    bucket_name = "pie-gpt"
    object_key = "datasets/whisper/whisper.zip"

    try:
        http_url = generate_signed_url(
            "PGBDWTGHUYVBATLBFF6S",
            "APLMZtd8eiCQixoS3klfY0EmGljQykS6mhzDc2b6",
            "https://obs.cn-north-4.myhuaweicloud.com",
            bucket_name,
            object_key,
        )
        print("Generated HTTP URL:", http_url)
    except Exception as e:
        print("An error occurred while generating the signed URL.")
        print(e)
