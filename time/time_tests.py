from datetime import datetime


def format_int():
    # 获取当前时间并格式化为 年-月-日 时:分:秒
    current_time = datetime.now().strftime('%m%d%H%M')
    print(current_time)  # 输出示例: 2024-01-12 15:30:45


if __name__ == "__main__":
    format_int()
