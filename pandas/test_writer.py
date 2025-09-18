import pandas as pd
import re

# 创建一个示例 DataFrame
data = {
    'Product': ['Apple', 'Banana', 'Orange'],
    'Size': ['13113  ', '13,113', '30% 70%'],
    'Price': [2.99, 1.50, 0.75]
}
df = pd.DataFrame(data)
print("原始 DataFrame:")
print(df)


# 定义一个函数来提取数值和单位
def split_size(size_str):
    # 使用正则表达式匹配数值和非数值部分
    # \d+(\.\d+)? 匹配整数或带小数的数字
    # \s* 匹配可选的空格
    # (.*) 匹配单位部分
    match = re.search(r'^(\d+\.?\d*)\s*(\w+)$', str(size_str).strip())
    if match:
        value = float(match.group(1))  # 提取数值并转换为浮点型
        unit = match.group(2).strip()  # 提取单位并去除首尾空格
        return value, unit
    return size_str, None  # 如果匹配失败，返回 None


regex = r'^(\d+\.?\d*)\s*(\w+)$'

# 对 'Size' 列应用函数，将结果赋给新列
df[['Size_Value', 'Size_Unit']] = df['Size'].apply(lambda x: pd.Series(split_size(x)))

# 对 'Size' 列应用 .str.extract() 方法
# 这是一种更简洁的提取方式，它直接将捕获组提取为新的列
# df[['Size_Value', 'Size_Unit']] = df['Size'].str.extract(regex).astype({'Size_Value': 'float'})

# (可选) 删除原始的 'Size' 列
# df = df.drop(columns=['Size'])

# 导出到 Excel
# 你也可以指定 sheet_name 等参数
# df.to_excel('product_info.xlsx', index=False)
# print("\n数据已成功导出到 product_info.xlsx")

print("\n处理后的 DataFrame:")
print(df)
