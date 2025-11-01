import glob
import os


def find_files_glob_recursive(dir, keyword):
    # 构建模式：** 表示匹配所有子目录，然后是 *keyword*
    pattern = os.path.join(dir, f"**/*{keyword}*")
    # recursive=True 启用递归查找
    found_files = glob.glob(pattern, recursive=True)
    return found_files


if __name__ == '__main__':
    target_dir = "/mnt/work/code/extractor/pdf-extractor/output/Fanning和O'Neill - 2016 - Tracking resource use relative to planetary boundaries in a steady-state framework A case study of"
    keyword = "Figure"
    files = find_files_glob_recursive(target_dir, keyword)
    print(f"在目录 '{target_dir}' 及其子目录下，文件名包含 '{keyword}' 的文件:")
    for file in files:
        print(file)
