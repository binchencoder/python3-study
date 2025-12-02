import pandas as pd
import numpy as np
import os

# 假设文件路径和常量定义
# 注意：此处的路径是您代码中指定的路径
FILE_NAME = '/mnt/work/code/extractor/DATA/小作物播种面积调整_.xlsx'

PROVINCE = 'Liaoning'  # 2022/2017数据中的省份名
PROVINCE_CN = '辽宁'  # 统计年鉴中的省份名
CROP_2022 = 'peanut_sown_area(1000 hectares)'  # 2022年花生面积列名
CROP_2017 = 'peanut_sown_area'  # 2017年花生面积列名
CROP_REF = '花生'  # 统计年鉴中的花生列名
CITY_DATA_COL = 'City'  # 2022/2017数据中的城市列名
COUNTY_DATA_COL = 'County'  # 区县列名

# 调整比例阈值
RATIO_MIN_1 = 0.95
RATIO_MAX_1 = 1.05
RATIO_MIN_2 = 0.90
RATIO_MAX_2 = 1.10


def clean_numeric_col(df, col):
    """将指定列转换为数值类型，并将 NaN 填充为 0。"""
    if col in df.columns:
        # 清理可能的逗号或空格，然后强制转为数值
        df[col] = df[col].astype(str).str.replace(',', '', regex=False).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # 将 NaN 视为空白或零面积
        df[col] = df[col].fillna(0)
    return df


def load_data():
    """加载所有数据文件并进行初步清洗，并处理辽宁统计年鉴缺失的情况。"""
    try:
        # 1. 加载区县数据（假设单行头）
        df_2022 = pd.read_excel(FILE_NAME, sheet_name="2022-crop-sown area")
        df_2017 = pd.read_excel(FILE_NAME, sheet_name="2017-crop-sown area")

        # 2. 加载国家统计年鉴数据（假设第二行是头，即 header=1）
        df_national_ref = pd.read_excel(FILE_NAME, sheet_name="国家统计年鉴小作物种植面积", header=1)
        df_national_ref.rename(columns={'省份': 'Province'}, inplace=True)

        # 3. 尝试加载辽宁省统计年鉴（市级参考数据）
        liaoning_ref_provided = True
        try:
            df_liaoning_ref = pd.read_excel(FILE_NAME, sheet_name="辽宁省统计年鉴", header=1)
            df_liaoning_ref.rename(columns={'地区': 'City_CN'}, inplace=True)
            print(f"注意: 工作表 '辽宁省统计年鉴' 已找到，使用提供的市级参考数据。")
        except ValueError:
            # 如果工作表不存在，则创建一个空的 DataFrame，并设置标志
            print(f"注意: 工作表 '辽宁省统计年鉴' 未找到。将尝试从区县数据计算市级参考值。")
            df_liaoning_ref = pd.DataFrame(columns=['City_CN', 'Placeholder_Ref'])  # 创建一个占位 DataFrame
            liaoning_ref_provided = False

        # 4. 清洗数值列
        df_2022 = clean_numeric_col(df_2022, CROP_2022)
        df_2017 = clean_numeric_col(df_2017, CROP_2017)
        df_national_ref = clean_numeric_col(df_national_ref, CROP_REF)
        df_liaoning_ref = clean_numeric_col(df_liaoning_ref, CROP_REF)

        # 5. 确保所有 City 列是字符串类型以便匹配
        df_2022[CITY_DATA_COL] = df_2022[CITY_DATA_COL].astype(str)
        df_2017[CITY_DATA_COL] = df_2017[CITY_DATA_COL].astype(str)
        # 只有在加载成功时才处理 City_CN，否则它可能缺失
        if liaoning_ref_provided and 'City_CN' in df_liaoning_ref.columns:
            df_liaoning_ref['City_CN'] = df_liaoning_ref['City_CN'].astype(str)

        return df_2022, df_2017, df_national_ref, df_liaoning_ref, liaoning_ref_provided

    except FileNotFoundError as e:
        print(f"错误: 文件未找到，请检查路径是否正确: {e.filename}")
        raise
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        raise


def process_data(df_2022, df_2017, df_national_ref, df_liaoning_ref, liaoning_ref_provided):
    """执行所有调整逻辑。"""
    df_adjusted = df_2022.copy()

    # 过滤出 2022 年辽宁省所有区县数据
    df_liaoning_data = df_adjusted[df_adjusted['Province'] == PROVINCE].copy()

    # --- 2. 省份层面检查 (AO20/C8) ---

    # 2.1 计算 AO20 (2022 辽宁花生面积总和)
    AO20 = df_liaoning_data[CROP_2022].sum()
    print(f"1. 2022 辽宁省花生面积（区县总和 AO20）: {AO20:.4f} 千公顷")

    # 2.2 查找 C8 (国家统计年鉴 辽宁花生面积)
    C8_series = df_national_ref[df_national_ref['Province'] == PROVINCE_CN][CROP_REF]
    C8 = C8_series.iloc[0] if not C8_series.empty else np.nan

    print(f"   国家统计年鉴 {PROVINCE_CN} 花生数据 (C8): {C8:.4f} 千公顷")

    needs_city_adjustment = True
    if not np.isnan(C8) and C8 > 0 and AO20 > 0:
        ratio_province = AO20 / C8
        print(f"   AO20/C8 比例: {ratio_province:.4f}")

        if RATIO_MIN_1 <= ratio_province <= RATIO_MAX_1:
            print(f"   比例在 [{RATIO_MIN_1}, {RATIO_MAX_1}] 范围内，无需市级调整。")
            needs_city_adjustment = False
        else:
            print(f"   比例不在 [{RATIO_MIN_1}, {RATIO_MAX_1}] 范围内，进行市级调整。")
    else:
        print("   C8 或 AO20 数据无效，跳过省份级检查，尝试市级调整或分解。")

    # --- 2.3 NEW: 如果市级参考数据缺失且需要调整，则进行分解计算 ---
    if not liaoning_ref_provided and needs_city_adjustment:
        if not np.isnan(C8) and C8 > 0 and AO20 > 0:
            print("\n--- 2.3 辽宁省统计年鉴数据缺失，根据2022区县数据比例进行分解计算市级参考值 (B) ---")

            # 1. 计算每个 City_DATA_COL 中的城市总和 A
            df_city_sums = df_liaoning_data.groupby(CITY_DATA_COL)[CROP_2022].sum().reset_index()

            # 2. 计算城市权重 (A_Sum / AO20)
            df_city_sums['Weight'] = df_city_sums[CROP_2022] / AO20

            # 3. 计算衍生市级参考值 B_derived = C8 * Weight
            df_city_sums[CROP_REF] = df_city_sums['Weight'] * C8

            # 准备新的 df_liaoning_ref 结构（使用 2022 数据中的 City 列作为 City_CN）
            df_liaoning_ref = df_city_sums.rename(columns={CITY_DATA_COL: 'City_CN'})[['City_CN', CROP_REF]]

            print(f"   已根据 AO20 ({AO20:.4f}) 和 C8 ({C8:.4f}) 衍生出 {len(df_liaoning_ref)} 个市级参考值。")
        else:
            print("\n--- 警告：无法推算市级参考值 B (C8 或 AO20 无效)。跳过市级调整。---")
            needs_city_adjustment = False

    # --- 3. 市级调整逻辑 (统一使用 df_liaoning_ref) ---
    city_adjustment_log = []

    if needs_city_adjustment and 'City_CN' in df_liaoning_ref.columns:

        # 排除总计行和空值
        liaoning_cities_ref = df_liaoning_ref['City_CN'].unique()
        liaoning_cities_ref = [c for c in liaoning_cities_ref if c not in ['全省', '地区', 'nan', np.nan]]

        for city_cn in liaoning_cities_ref:

            # 3.1 查找 B (市级花生面积)
            B_series = df_liaoning_ref[df_liaoning_ref['City_CN'] == city_cn][CROP_REF]
            B = B_series.iloc[0] if not B_series.empty else 0.0

            # --- 匹配 2022 数据中的 City 列 ---
            if liaoning_ref_provided:
                # 原始数据（统计年鉴）使用模糊匹配，例如 '鞍山' 匹配 '鞍山市'
                city_match_name = city_cn.replace('市', '').replace('地区', '')
                df_city_data = df_liaoning_data[
                    df_liaoning_data[CITY_DATA_COL].str.contains(city_match_name, na=False)
                ].copy()
            else:
                # 推算数据，City_CN 就是 2022 数据中的 City，使用精确匹配
                df_city_data = df_liaoning_data[df_liaoning_data[CITY_DATA_COL] == city_cn].copy()

            if df_city_data.empty or B <= 0:
                city_adjustment_log.append({
                    'City': city_cn, 'County_Sum (A)': 0, 'Ref_Data (B)': B,
                    'A/B Ratio': np.nan, 'Status': 'Skipped (Data or Reference B is zero/missing)'
                })
                continue

            city_name_in_data = df_city_data[CITY_DATA_COL].iloc[0]  # 获取 2022 数据中实际的城市名

            # 3.2 计算 A (2022 区县数据 市级花生面积总和)
            A = df_city_data[CROP_2022].sum()
            ratio_city = A / B

            log_entry = {
                'City': city_name_in_data,
                'County_Sum (A)': A,
                'Ref_Data (B)': B,
                'A/B Ratio': ratio_city,
                'Status': ''
            }

            # 3.3 比例判断与调整
            if RATIO_MIN_1 <= ratio_city <= RATIO_MAX_1:
                log_entry['Status'] = 'No Adjustment (Ratio within 0.95-1.05)'

            elif ratio_city < RATIO_MIN_2 or ratio_city > RATIO_MAX_2:
                log_entry['Status'] = f'Marked (Ratio < {RATIO_MIN_2} or > {RATIO_MAX_2})'

            elif RATIO_MIN_2 <= ratio_city < RATIO_MIN_1 or RATIO_MAX_1 < ratio_city <= RATIO_MAX_2:
                log_entry[
                    'Status'] = f'Adjustment needed (Ratio in [{RATIO_MIN_2}, {RATIO_MIN_1}) or ({RATIO_MAX_1}, {RATIO_MAX_2}])'

                # --- 4. 执行调整 (逻辑不变) ---
                difference = B - A

                # 1. 筛选出 2022 年该市花生面积为 0 的区县
                df_city_2022_zero = df_city_data[
                    df_city_data[CROP_2022] == 0
                    ]

                # 2. 匹配 2017 年数据，获取调整基数
                counties_to_adjust = df_city_2022_zero[COUNTY_DATA_COL].tolist()

                df_city_2017_base = df_2017[
                    (df_2017[CITY_DATA_COL] == city_name_in_data) &
                    (df_2017[COUNTY_DATA_COL].isin(counties_to_adjust))
                    ].copy()

                S_2017 = df_city_2017_base[CROP_2017].sum()

                if S_2017 > 0 and not df_city_2017_base.empty:

                    # 计算调整比例和调整量
                    df_city_2017_base['Adjustment_Ratio'] = df_city_2017_base[CROP_2017] / S_2017
                    df_city_2017_base['Adjustment'] = difference * df_city_2017_base['Adjustment_Ratio']

                    # 4. 更新 df_adjusted 中的数据
                    for index, row in df_city_2017_base.iterrows():
                        county = row[COUNTY_DATA_COL]
                        adjustment = row['Adjustment']

                        condition = (df_adjusted[CITY_DATA_COL] == city_name_in_data) & \
                                    (df_adjusted[COUNTY_DATA_COL] == county) & \
                                    (df_adjusted['Province'] == PROVINCE)

                        # 原始值是 0，新值就是调整量
                        df_adjusted.loc[condition, CROP_2022] = adjustment.round(4)

                    # 5. 检查一致性 (重新计算调整后的总和)
                    A_new = df_adjusted[
                        (df_adjusted[CITY_DATA_COL] == city_name_in_data) &
                        (df_adjusted['Province'] == PROVINCE)
                        ][CROP_2022].sum()

                    log_entry['Check (New A/B)'] = f"{A_new:.4f} / {B:.4f} = {A_new / B:.4f}"
                    log_entry['Status'] += f" | Adjusted. New Sum: {A_new:.4f}"

                else:
                    log_entry['Status'] += ' | Adjustment Failed - 2017 base S_2017 is zero or missing.'

            city_adjustment_log.append(log_entry)

    # --- 5. 结果汇总与输出 ---
    print("\n--- 2. 市级调整日志及结果 (Liaoning / 花生) ---")
    log_df = pd.DataFrame(city_adjustment_log)
    print(log_df.to_markdown(index=False))

    # 最终检查调整后的省份总和
    AO20_new = df_adjusted[df_adjusted['Province'] == PROVINCE][CROP_2022].sum()
    if not np.isnan(C8) and C8 > 0:
        ratio_province_new = AO20_new / C8
        print(f"\n3. 最终结果：调整后 {PROVINCE_CN} 花生面积总和: {AO20_new:.4f} 千公顷")
        print(f"   调整后 AO20_new/C8 比例: {ratio_province_new:.4f}")

    # 保存最终结果到 Excel
    output_file_name = '2022_crop_sown_area_adjusted_peanut_liaoning.xlsx'
    df_adjusted.to_excel(output_file_name, index=False)
    print(f"\n数据处理完成。调整后的数据已保存到文件: {output_file_name}")

    return output_file_name


if __name__ == '__main__':
    # --- 运行主程序 ---
    try:
        # load_data 返回包含一个布尔值 liaoning_ref_provided
        df_2022, df_2017, df_national_ref, df_liaoning_ref, liaoning_ref_provided = load_data()
        output_file = process_data(df_2022, df_2017, df_national_ref, df_liaoning_ref, liaoning_ref_provided)

    except Exception as e:
        print(f"程序执行失败: {e}")
