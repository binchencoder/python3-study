import pandas as pd
import numpy as np
import os

# 假设文件路径
# FILE_NAME = '/Volumes/BinchenCoder/python_workspace/extractor/LIULING/小作物播种面积调整.xlsx'
FILE_NAME = '/mnt/work/code/extractor/DATA/小作物播种面积调整_.xlsx'

# --- 核心列名常量 ---
COL_NAME_CITY = 'City'  # 2022/2017数据中的城市列名
COL_NAME_COUNTY = 'County'  # 区县列名
COL_NAME_PROVINCE = 'Province'

# 调整比例阈值
RATIO_MIN_1 = 0.95
RATIO_MAX_1 = 1.05
RATIO_MIN_2 = 0.90
RATIO_MAX_2 = 1.10

# 定义需要处理"省统计年鉴"表的列名
COLS_CITY = [
    'Province',
    'City'
    'nonbeans_sown_area(1000 hectares)',
    'millet_sown_area(1000 hectares)',
    'sorghum_sown_area(1000 hectares)',
    'othercereals_sown_area(1000 hectares)',
    'potato_sown_area(1000 hectares)',
    'peanut_sown_area(1000 hectares)',
    'rapeseed_sown_area(1000 hectares)',
    'cotton_sown_area(1000 hectares)',
    'flax_sown_area(1000 hectares)',
    'sugarcane_sown_area(1000 hectares)',
    'sugarbeet_sown_area(1000 hectares)',
    'tobacco_sown_area(1000 hectares)',
    'vegetable_sown_area(1000 hectares)',
    'fruittree_sown_area(1000 hectares)',
    'greenfodder_sown_area(1000 hectares)',
    'managedgrass_sown_area(1000 hectares)',
    'naturalgrass_sown_area(1000 hectares)',
]

# --- 辅助：中英文省份名称映射表 (保持不变) ---
PROVINCE_MAP = {
    'Beijing': ':北京',
    'Tianjin': '天津',
    'Hebei': '河北',
    'Shanxi': '山西',
    'Inner Mongolia': '内蒙古',
    'Liaoning': '辽宁',
    'Jilin': '吉林',
    'Heilongjiang': '黑龙江',
    'Shanghai': '上海',
    'Jiangsu': '江苏',
    'Zhejiang': '浙江',
    'Anhui': '安徽',
    'Fujian': '福建',
    'Jiangxi': '江西',
    'Shandong': '山东',
    'Henan': '河南',
    'Hubei': '湖北',
    'Hunan': '湖南',
    'Guangdong': '广东',
    'Guangxi': '广西',
    'Hainan': '海南',
    'Chongqing': '重庆',
    'Sichuan': '四川',
    'Guizhou': '贵州',
    'Yunnan': '云南',
    'Tibet': '西藏',
    'Shaanxi': '陕西',
    'Gansu': '甘肃',
    'Qinghai': '青海',
    'Ningxia': '宁夏',
    'Xinjiang': '新疆',
    # 请在此处补充您数据中所有省份的映射
}

COL_CROP_NAME_MAP = {
    '花生': 'peanut_sown_area(1000 hectares)',
    '油菜籽': 'rapeseed_sown_area(1000 hectares)',
    '棉花': 'cotton_sown_area(1000 hectares)',
    '麻类': 'flax_sown_area(1000 hectares)',
    '甘蔗': 'sugarcane_sown_area(1000 hectares)',
    '甜菜': 'sugarbeet_sown_area(1000 hectares)',
    '烟叶': 'tobacco_sown_area(1000 hectares)',
    '蔬菜': 'vegetable_sown_area(1000 hectares)',
    '果园': 'fruittree_sown_area(1000 hectares)',
}

# --- 关键修改：作物列名映射表 ---
# 格式：{ '2022数据中的列名': ('2017数据中的列名', '统计年鉴中的列名') }
# 注意：2022数据中的列名可能包含单位 '(1000 hectares)'
CROP_COLUMN_MAP = {
    # 'nonbeans_sown_area(1000 hectares)':('nonbeans_sown_area', ''),
    # 'millet_sown_area(1000 hectares)':('millet_sown_area',''),
    # 'sorghum_sown_area(1000 hectares)':('sorghum_sown_area','高梁'),
    # 'othercereals_sown_area(1000 hectares)':('othercereals','其他杂粮'),
    # 'potato_sown_area(1000 hectares)':('potato','薯类'),
    'peanut_sown_area(1000 hectares)': ('peanut_sown_area', '花生'),
    'rapeseed_sown_area(1000 hectares)': ('rapeseed_sown_area', '油菜籽'),  # 假设要调整油菜籽
    'cotton_sown_area(1000 hectares)': ('cotton_sown_area', '棉花'),  # 假设要调整棉花
    'flax_sown_area(1000 hectares)': ('flax', '麻类'),
    'sugarcane_sown_area(1000 hectares)': ('sugarcane', '甘蔗'),
    'sugarbeet_sown_area(1000 hectares)': ('sugarbeet', '甜菜'),
    'tobacco_sown_area(1000 hectares)': ('tobacco', '烟叶'),
    'vegetable_sown_area(1000 hectares)': ('vegetable', '蔬菜'),
    'fruittree_sown_area(1000 hectares)': ('fruittree', '果园'),
    # 'greenfodder_sown_area(1000 hectares)':('greenfodder',''),
    # 'managedgrass_sown_area(1000 hectares)':('managedgrass',''),
    # 'naturalgrass_sown_area(1000 hectares)':('naturalgrass',''),

    # 请根据您的实际需求，补充需要进行调整的作物列
}


def clean_numeric_col(df, col):
    """将指定列转换为数值类型，并将 NaN 填充为 0。"""
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0)
    return df


def load_data():
    """加载所有数据文件，并尝试加载辽宁省统计年鉴。"""
    try:
        # 1. 加载区县数据
        df_2022 = pd.read_excel(FILE_NAME, sheet_name="2022-crop-sown area")
        df_2017 = pd.read_excel(FILE_NAME, sheet_name="2017-crop-sown area")

        # 2. 加载国家统计年鉴数据
        df_national_ref = pd.read_excel(FILE_NAME, sheet_name="国家统计年鉴小作物种植面积", header=1)
        df_national_ref.rename(columns={'省份': COL_NAME_PROVINCE}, inplace=True)

        # rename_cols = COL_CROP_NAME_MAP.copy()
        # rename_cols.update({'省份': COL_NAME_PROVINCE})
        # df_national_ref.rename(columns=rename_cols, inplace=True)

        # 3. 尝试加载辽宁省统计年鉴
        liaoning_ref_provided = True
        try:
            df_liaoning_ref = pd.read_excel(FILE_NAME, sheet_name="辽宁省统计年鉴", header=1)
            df_liaoning_ref.rename(columns={'地区': 'City_CN'}, inplace=True)

            # rename_cols = COL_CROP_NAME_MAP.copy()
            # rename_cols.update({'地区': 'City_CN'})
            # df_liaoning_ref.rename(columns=rename_cols, inplace=True)
            print(f"注意: 工作表 '辽宁省统计年鉴' 已找到，将用于辽宁省的市级参考。")
        except ValueError:
            print(f"注意: 工作表 '辽宁省统计年鉴' 未找到。所有省份的市级参考值将通过分解国家级数据得到。")
            df_liaoning_ref = pd.DataFrame()
            liaoning_ref_provided = False

        # 4. 清洗数值列
        # 对所有潜在需要调整的作物列进行清洗
        all_crop_cols = (set(CROP_COLUMN_MAP.keys())
                         | set(col[0] for col in CROP_COLUMN_MAP.values())
                         | set(col[1] for col in CROP_COLUMN_MAP.values())
                         )

        for col in all_crop_cols:
            df_2022 = clean_numeric_col(df_2022, col)
            df_2017 = clean_numeric_col(df_2017, col)
            df_national_ref = clean_numeric_col(df_national_ref, col)
            df_liaoning_ref = clean_numeric_col(df_liaoning_ref, col)

        # 5. 确保 City/Province 列为字符串
        for df in [df_2022, df_2017]:
            df[COL_NAME_CITY] = df[COL_NAME_CITY].astype(str)
            df[COL_NAME_PROVINCE] = df[COL_NAME_PROVINCE].astype(str)

        return df_2022, df_2017, df_national_ref, df_liaoning_ref, liaoning_ref_provided

    except FileNotFoundError as e:
        print(f"错误: 文件未找到，请检查路径是否正确: {e.filename}")
        raise
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        raise


def generate_province_statistical_table():
    pass


def process_data_for_all_crops_and_provinces(df_2022, df_2017, df_national_ref, df_liaoning_ref, liaoning_ref_provided):
    """循环遍历所有作物和所有省份，执行调整逻辑。"""

    # 最终调整后的数据副本 (在每个作物循环开始时创建，以便在 df_2022 上进行操作)
    df_adjusted_all = df_2022.copy()
    all_adjustment_logs = []

    # 获取所有需要处理的省份 (英文名)
    provinces_to_process = df_2022[COL_NAME_PROVINCE].unique()

    print(f"--- 发现 {len(CROP_COLUMN_MAP)} 种作物，{len(provinces_to_process)} 个省份需要处理 ---")

    # --- 外层循环：遍历所有作物 ---
    for crop_2022_col, (crop_2017_col, crop_ref_col) in CROP_COLUMN_MAP.items():

        CROP_2022 = crop_2022_col
        CROP_2017 = crop_2017_col
        CROP_REF = crop_ref_col

        print(f"\n\n#######################################################")
        print(f"### 开始调整作物：{CROP_REF} ({CROP_2022}) ###")
        print(f"#######################################################")

        # --- 内层循环：遍历所有省份 ---
        for province_en in provinces_to_process:
            if province_en != 'Liaoning':
                continue

            province_cn = PROVINCE_MAP.get(province_en)
            if not province_cn:
                print(f"\n警告: 未找到省份 '{province_en}' 的中文名称映射，跳过此省份调整。")
                continue

            print(f"\n=======================================================")
            print(f"开始处理 {CROP_REF} 在省份: {province_cn} ({province_en}) 的数据")
            print(f"=======================================================")

            # 过滤出 2022 年当前省份的所有区县数据
            # 注意：此处使用 df_adjusted_all，确保上一省份/作物调整的结果得以保留
            df_province_data = df_adjusted_all[df_adjusted_all[COL_NAME_PROVINCE] == province_en].copy()

            # --- 2. 省份层面检查 (AO20/C8) ---
            AO20 = df_province_data[CROP_2022].sum()
            C8_series = df_national_ref[df_national_ref[COL_NAME_PROVINCE] == province_cn][CROP_REF]
            C8 = C8_series.iloc[0] if not C8_series.empty else np.nan

            print(f"1. 2022 {province_cn} {CROP_REF} 面积 (区县总和 AO20): {AO20:.4f} 千公顷")
            print(f"   国家统计年鉴 {province_cn} {CROP_REF} 数据 (C8): {C8:.4f} 千公顷")

            needs_city_adjustment = True
            if not np.isnan(C8) and C8 > 0 and AO20 > 0:
                ratio_province = AO20 / C8
                print(f"   AO20/C8 比例: {ratio_province:.4f}")

                if RATIO_MIN_1 <= ratio_province <= RATIO_MAX_1:
                    print(f"   比例在 [{RATIO_MIN_1}, {RATIO_MAX_1}] 范围内，无需市级调整。")
                    needs_city_adjustment = False
                    continue
                else:
                    print(f"   比例不在 [{RATIO_MIN_1}, {RATIO_MAX_1}] 范围内，进行市级调整。")
            else:
                print("   C8 或 AO20 数据无效，跳过省份级检查，无法进行市级调整。")
                needs_city_adjustment = False
                continue

            # --- 2.3 确定市级参考数据 (B) ---
            df_city_ref = pd.DataFrame()

            # 优先使用提供的辽宁省统计年鉴（仅限辽宁）
            if liaoning_ref_provided and province_en == 'Liaoning' and not df_liaoning_ref.empty:
                # if CROP_REF in df_liaoning_ref.columns:
                df_city_ref = df_liaoning_ref.copy()
                print(f"--- 使用提供的 '辽宁省统计年鉴' {CROP_REF} 数据作为市级参考值 (B)。 ---")

            # 其他情况（包括辽宁年鉴缺失时）进行推算
            elif needs_city_adjustment:
                # 推算逻辑：按 2022 区县数据中的城市占比分解 C8
                print(f"--- 缺乏市级年鉴数据，根据2022区县数据比例分解 C8 ({province_cn}) ---")

                df_city_sums = df_province_data.groupby(COL_NAME_CITY)[CROP_2022].sum().reset_index()
                df_city_sums['Weight'] = df_city_sums[CROP_2022] / AO20
                df_city_sums[CROP_REF] = df_city_sums['Weight'] * C8
                df_city_ref = df_city_sums.rename(columns={COL_NAME_CITY: 'City_CN'})[['City_CN', CROP_REF]]

            # --- 3. 市级调整逻辑 (统一使用 df_city_ref) ---
            if needs_city_adjustment and not df_city_ref.empty:

                cities_to_process = [c for c in df_city_ref['City_CN'].unique() if
                                     c not in ['全省', '地区', 'nan', np.nan]]

                for city_cn in cities_to_process:

                    # 3.1 查找 B
                    B_series = df_city_ref[df_city_ref['City_CN'] == city_cn][CROP_REF] \
                        if CROP_REF in df_city_ref.columns else None
                    B = B_series.iloc[0] if B_series is not None else 0.0

                    # 确定 City 匹配方式
                    city_match_name = city_cn.replace('市', '').replace('地区', '')
                    if province_en == 'Liaoning' and liaoning_ref_provided:
                        df_city_data = df_province_data[
                            df_province_data[COL_NAME_CITY].str.contains(city_match_name, na=False)
                        ].copy()
                    else:
                        df_city_data = df_province_data[df_province_data[COL_NAME_CITY] == city_cn].copy()

                    if df_city_data.empty or B <= 0:
                        all_adjustment_logs.append({
                            'Crop': CROP_REF, COL_NAME_PROVINCE: province_en, 'City': city_cn, 'County_Sum (A)': 0,
                            'Ref_Data (B)': B,
                            'A/B Ratio': np.nan, 'Status': 'Skipped (Data or Reference B is zero/missing)'
                        })
                        continue

                    city_name_in_data = df_city_data[COL_NAME_CITY].iloc[0]
                    A = df_city_data[CROP_2022].sum()
                    ratio_city = A / B

                    log_entry = {
                        'Crop': CROP_REF,
                        'Province': province_en,
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
                        log_entry['Status'] = 'Adjustment needed'

                        # --- 4. 执行调整 ---
                        difference = B - A
                        df_city_2022_zero = df_city_data[df_city_data[CROP_2022] == 0]
                        counties_to_adjust = df_city_2022_zero[COL_NAME_COUNTY].tolist()

                        # 2. 匹配 2017 年数据 (注意使用 CROP_2017 列名)
                        df_city_2017_base = df_2017[
                            (df_2017[COL_NAME_CITY] == city_name_in_data) &
                            (df_2017[COL_NAME_PROVINCE] == province_en) &
                            (df_2017[COL_NAME_COUNTY].isin(counties_to_adjust))
                            ].copy()
                        S_2017 = df_city_2017_base[CROP_2017].sum()

                        if S_2017 > 0 and not df_city_2017_base.empty:
                            df_city_2017_base['Adjustment_Ratio'] = df_city_2017_base[CROP_2017] / S_2017
                            df_city_2017_base['Adjustment'] = difference * df_city_2017_base['Adjustment_Ratio']

                            # 4. 更新 df_adjusted_all 中的数据
                            for _, row in df_city_2017_base.iterrows():
                                county = row[COL_NAME_COUNTY]
                                adjustment = row['Adjustment']

                                condition = (df_adjusted_all[COL_NAME_CITY] == city_name_in_data) & \
                                            (df_adjusted_all[COL_NAME_COUNTY] == county) & \
                                            (df_adjusted_all[COL_NAME_PROVINCE] == province_en)

                                # 核心：动态更新 CROP_2022 所在的列
                                df_adjusted_all.loc[condition, CROP_2022] = adjustment.round(4)

                            # 5. 检查一致性
                            A_new = df_adjusted_all[
                                (df_adjusted_all[COL_NAME_CITY] == city_name_in_data) &
                                (df_adjusted_all[COL_NAME_PROVINCE] == province_en)
                                ][CROP_2022].sum()

                            log_entry['Check (New A/B)'] = f"{A_new:.4f} / {B:.4f} = {A_new / B:.4f}"
                            log_entry['Status'] += f" | Adjusted. New Sum: {A_new:.4f}"

                        else:
                            log_entry['Status'] += ' | Adjustment Failed - 2017 base S_2017 is zero or missing.'

                    all_adjustment_logs.append(log_entry)
            else:
                print(f"   {province_cn} {CROP_REF} 市级参考数据缺失或不需要调整，跳过市级循环。")

    # --- 5. 结果汇总与输出 ---
    print("\n\n#######################################################")
    print("### 最终处理结果汇总：市级调整日志 (所有作物/所有省份) ###")
    print("#######################################################")
    log_df = pd.DataFrame(all_adjustment_logs)
    print(log_df.to_markdown(index=False))
    output_log_file_name = '2022_crop_sown_area_adjusted_log.xlsx'
    log_df.to_excel(output_log_file_name, index=False)

    # 最终检查并输出省份总和
    print(f"\n\n#######################################################")
    print(f"### 3. 最终省份/作物总和检查 ###")
    print(f"#######################################################")
    final_check(df_adjusted_all, df_national_ref, provinces_to_process)

    # 保存最终结果到 Excel
    output_file_name = '2022_crop_sown_area_adjusted_all_crops_and_provinces.xlsx'
    df_adjusted_all.to_excel(output_file_name, index=False)
    print(f"\n数据处理完成。调整后的数据已保存到文件: {output_file_name}")

    return output_file_name


def final_check(df_adjusted_all, df_national_ref, provinces_to_process):
    for crop_2022_col, (_, crop_ref_col) in CROP_COLUMN_MAP.items():
        CROP_REF = crop_ref_col
        print(f"\n--- {CROP_REF} 调整后总和 ---")
        for province_en in provinces_to_process:
            province_cn = PROVINCE_MAP.get(province_en)
            if not province_cn:
                continue
            if province_en != 'Liaoning':
                continue

            AO20_new = df_adjusted_all[df_adjusted_all[COL_NAME_PROVINCE] == province_en][crop_2022_col].sum()
            C8_series = df_national_ref[df_national_ref[COL_NAME_PROVINCE] == province_cn][CROP_REF]
            C8 = C8_series.iloc[0] if not C8_series.empty else np.nan

            if not np.isnan(C8) and C8 > 0:
                ratio_province_new = AO20_new / C8
                print(
                    f"   {province_cn} 调整后总和: {AO20_new:.4f} 千公顷 | 调整后比例 (AO20/C8): {ratio_province_new:.4f}")
            else:
                print(f"   {province_cn} 调整后总和: {AO20_new:.4f} 千公顷 | C8数据缺失。")


if __name__ == '__main__':
    # --- 运行主程序 ---
    try:
        df_2022, df_2017, df_national_ref, df_liaoning_ref, liaoning_ref_provided = load_data()
        output_file = process_data_for_all_crops_and_provinces(df_2022, df_2017, df_national_ref, df_liaoning_ref,
                                                               liaoning_ref_provided)

    except Exception as e:
        print(f"程序执行失败: {e}")
