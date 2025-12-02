import pandas as pd
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

file_name = "/mnt/work/code/extractor/DATA/工作簿1.xlsx"

# 1. 读取文件
try:
    df = pd.read_excel(file_name, "Sheet1")
except Exception as e:
    print(f"读取文件 {file_name} 失败: {e}")
    # 假设文件读取成功，继续后续步骤

# 2. 识别需要求和的数值列 (排除 Province 和可能存在的非数值标识列)
# 先将所有列转换为数值类型，无法转换的设为 NaN，然后求和时自动跳过非数值列
for col in df.columns:
    if col != 'Province':
        # 强制转换为数值类型，errors='coerce' 将无法转换的值设为 NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 3. 按 'Province' 分组计算总和
df_sum = df.groupby('Province').sum(numeric_only=True).reset_index()

try:
    with pd.ExcelWriter(file_name, engine='openpyxl', mode='a',
                        if_sheet_exists='overlay') as writer:  # 注意：需要安装 openpyxl 库
        # 关键参数：
        # startrow=start_row: 指定从哪一行开始写入数据
        # header=header: 控制是否写入表头
        df_sum.to_excel(
            writer,
            sheet_name="SUM",
            header=True,
            index=False  # 不写入 Pandas 索引
        )

        # df.to_excel(writer, sheet_name=f"{sheet_name}", index=False)
except PermissionError as e:
    logger.error(f"❌ 无法写入 {file_name}，请确认文件未被占用！{e}")
    raise e
except Exception as e:
    logger.error(f"❌❌❌❌❌ Failed to write excel {e}")
    raise e
