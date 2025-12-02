import pandas as pd
import numpy as np

# 读取区县数据
try:
    df_county = pd.read_excel("/mnt/work/code/extractor/DATA/2022crop production new (副本).xlsx", "区县数据")
except Exception as e:
    print(f"读取区县数据文件失败: {e}")
    # 假设 df_county 成功读取，继续后续步骤

# 读取省份统计数据
try:
    df_province = pd.read_excel("/mnt/work/code/extractor/DATA/2022crop production new (副本).xlsx", "省份统计")
except Exception as e:
    print(f"读取省份统计数据文件失败: {e}")
    # 假设 df_province 成功读取，继续后续步骤

# 定义需要处理的列名（区县数据和省份开源数据）
cols_to_adjust = [
    'Nitrogen Fertilizer Application(10,000 tons)',
    'Phosphate Fertilizer Application(10,000 tons)',
    'Potassium Fertilizer Application(10,000 tons)',
    'compound Application(10,000 tons)'
]

cols_sum_province_source = [
    '开源Nitrogen Fertilizer Application(10000 tons)',
    '开源Phosphate Fertilizer Application(10000 tons)',
    '开源Potassium Fertilizer Application(10000 tons)',
    '开源compound Application(10000 tons)'
]

# 统一列名映射，方便后续循环
col_map = dict(zip(cols_to_adjust, cols_sum_province_source))

# 将所有需要计算的列转换为数值类型，无法转换的设为 NaN
for col in cols_to_adjust:
    df_county[col] = pd.to_numeric(df_county[col], errors='coerce')

for col in cols_sum_province_source:
    df_province[col] = pd.to_numeric(df_province[col], errors='coerce')

# 1. 计算区县数据的省份总和
df_county_sum = df_county.groupby('Province')[cols_to_adjust].sum().reset_index()
df_county_sum.columns = ['Province'] + [f'{col}_Sum' for col in cols_to_adjust]

# 2. 合并数据，匹配区县总和与开源数据
df_ratio = pd.merge(
    df_county_sum,
    df_province[['Province'] + cols_sum_province_source],
    on='Province',
    how='left'
)

# 3. 计算调整比例
for original_col, open_source_col in col_map.items():
    sum_col = f'{original_col}_Sum'
    ratio_col = f'{original_col}_Ratio'

    # 确保分母不为 0
    # ratio = 开源数据 / 区县总和

    # 场景 1: 区县总和 > 0
    condition_positive = df_ratio[sum_col] > 0
    df_ratio.loc[condition_positive, ratio_col] = (
            df_ratio.loc[condition_positive, open_source_col] /
            df_ratio.loc[condition_positive, sum_col]
    )

    # 场景 2: 区县总和 == 0
    # 如果总和为 0，则比例无法计算。根据“保持比例不变”的原则，所有区县的值应为 0。
    # 如果开源数据也为 0，则比例设为 1，最终结果仍为 0。
    # 如果开源数据不为 0，则所有区县值需进行特殊调整（例如：平均分配），但这破坏了比例不变性，
    # 因此对于 sum=0 的情况，我们设定 ratio=0
    # **或者** 设定 ratio=1 并在后面通过 np.where(ratio * original_value) 来处理 NaN 或 0
    # 最稳健的方法是：如果 sum == 0 且 open_source != 0，则我们无法保持比例不变。
    # 如果 sum == 0 且 open_source == 0，则 ratio = 1 (最终 0 * 1 = 0)

    # 采取稳健处理：如果 sum <= 0，则比例设为 NaN，稍后通过 .fillna(0) 或特定逻辑处理
    df_ratio.loc[df_ratio[sum_col].le(0), ratio_col] = np.nan

# 提取省份和比例的映射
df_ratios_only = df_ratio[['Province'] + [f'{col}_Ratio' for col in cols_to_adjust]]

# 将比例合并到区县数据中
df_adjusted = pd.merge(
    df_county,
    df_ratios_only,
    on='Province',
    how='left'
)

# 应用调整
for original_col, open_source_col in col_map.items():
    ratio_col = f'{original_col}_Ratio'

    # 获取该省份原始总和是否为 0 的信息
    sum_col = f'{original_col}_Sum'
    # 将 df_ratio 的相关列合并回来，用于特殊情况判断
    df_adjusted = pd.merge(
        df_adjusted,
        df_ratio[['Province', sum_col, open_source_col]],
        on='Province',
        how='left'
    )

    # **核心调整逻辑**
    # 1. 正常情况：原始值 * 比例
    # 2. 省份总和为 0 (sum_col <= 0):
    #    - 如果开源数据 open_source_col 也为 0，则调整后值应为 0。
    #    - 如果开源数据 open_source_col 不为 0，且原始区县值为 0，调整后值应为 0。
    #
    # 我们将原始值（可能为 NaN 或 0）先填充为 0 进行计算，并使用 `fillna(0)` 确保 Ratio 列中的 NaN (来自分母为 0) 被有效处理。

    # 填充原始值中的 NaN 为 0
    df_adjusted[original_col] = df_adjusted[original_col].fillna(0)

    # 获取比例（Ratio）。对于分母为 0 的情况，Ratio 仍为 NaN。
    current_ratio = df_adjusted[ratio_col]

    # 特殊处理：如果 Ratio 是 NaN（因为原始总和为 0 或缺失）：
    #   - 如果开源数据也为 0 或 NaN，则最终值应为 0。
    #   - 如果开源数据不为 0：这个场景下，所有区县原始值都是 0，但总目标不为 0。
    #     由于要求“保持比例不变”，这在数学上是矛盾的（0/0 无法定义）。
    #     最佳实践是**平均分配**到所有区县，但为了严格满足“保持比例不变”的要求，
    #     我将坚持：**如果一个省份的总和为 0，那么调整后的所有区县值也应为 0**，以保持 $0/0$ 的比例，除非开源值也是 0。

    # 最终值计算：
    adjusted_values = df_adjusted[original_col] * current_ratio.fillna(0)

    # 重新赋值给原始列名, 保留三位小数
    df_adjusted[original_col] = adjusted_values.round(3)

    # 删除临时比例列和总和列
    df_adjusted = df_adjusted.drop(columns=[ratio_col, sum_col, open_source_col])

# 删除可能存在的重复列
df_adjusted = df_adjusted.loc[:, ~df_adjusted.columns.duplicated()].copy()

# 将 DataFrame 转换为 CSV 格式
adjusted_csv = df_adjusted.to_csv(index=False, encoding='utf-8')
print(adjusted_csv)
