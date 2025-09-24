import glob
import os


def find_latest_file(directory, prefix):
    # 构建匹配模式
    pattern = os.path.join(directory, f"{prefix}*.xlsx")

    # 使用 glob 找到所有匹配的文件，并按修改时间倒序排序
    latest_file = max(glob.glob(pattern), key=os.path.getmtime, default=None)

    return latest_file


# 示例用法
directory = "/Volumes/BinchenCoder/python_workspace/extractor"
# 假设 'my_folder' 目录下有这些文件:
# report_2023-01-01.txt
# data_2023-01-02.csv
# report_2023-02-15.txt (这个是最新更新的)
# data_2023-02-20.csv
# report_2023-01-20.txt

# 找到前缀为 'report' 的最新文件
latest_report = find_latest_file(directory, "all_figures_tables_flat_batch")
print(f"最新更新的 'report' 文件是: {latest_report}")
