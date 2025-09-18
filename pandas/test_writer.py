import pandas as pd
import re

# 创建一个示例 DataFrame
data = {'Product': ['Apple', 'Banana', 'Orange'],
        'Size': ['100 g', '2.5 kg', '这不是数字'],
        'Price': [2.99, 1.50, 0.75]}
df = pd.DataFrame(data)

print("原始 DataFrame:")
print(df)


# 定义一个函数来提取数值和单位
def split_size(size_str):
    # 使用正则表达式匹配数值和非数值部分
    # \d+(\.\d+)? 匹配整数或带小数的数字
    # \s* 匹配可选的空格
    # (.*) 匹配单位部分
    match = re.search(r'(\d+\.?\d*)\s*(.*)', str(size_str))
    if match:
        value = float(match.group(1))  # 提取数值并转换为浮点型
        unit = match.group(2).strip()  # 提取单位并去除首尾空格
        return value, unit
    return size_str, None  # 如果匹配失败，返回 None


# 对 'Size' 列应用函数，将结果赋给新列
df[['Size_Value', 'Size_Unit']] = df['Size'].apply(lambda x: pd.Series(split_size(x)))

# (可选) 删除原始的 'Size' 列
df = df.drop(columns=['Size'])

# 导出到 Excel
# 你也可以指定 sheet_name 等参数
# df.to_excel('product_info.xlsx', index=False)
# print("\n数据已成功导出到 product_info.xlsx")

print("\n处理后的 DataFrame:")
print(df)
