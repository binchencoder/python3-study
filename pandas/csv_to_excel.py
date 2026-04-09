import pandas as pd
import os
from io import StringIO


def csv_to_excel():
    csv = """
    Figure,Year,Region,Legend,Indicator,X,Y,Unit
    Water Distribution,,,Sulfonamides,f,0.0,0.33,
    Water Distribution,,,Sulfonamides,f,0.1,0.41,
    Water Distribution,,,Sulfonamides,f,0.2,0.50,
    Water Distribution,,,Sulfonamides,f,0.3,0.59,
    Water Distribution,,,Sulfonamides,f,0.4,0.66,
    Water Distribution,,,Sulfonamides,f,0.5,0.72,
    Water Distribution,,,Sulfonamides,f,0.6,0.76,
    Water Distribution,,,Sulfonamides,f,0.7,0.78,
    Water Distribution,,,Sulfonamides,f,0.8,0.79,
    Water Distribution,,,Sulfonamides,f,0.9,0.77,
    Water Distribution,,,Sulfonamides,f,1.0,0.74,
    Water Distribution,,,Sulfonamides,f,1.1,0.68,
    Water Distribution,,,Sulfonamides,f,1.2,0.61,
    Water Distribution,,,Sulfonamides,f,1.3,0.53,
    Water Distribution,,,Sulfonamides,f,1.4,0.45,
    Water Distribution,,,Sulfonamides,f,1.5,0.37,
    Water Distribution,,,Sulfonamides,f,1.6,0.29,
    Water Distribution,,,Sulfonamides,f,1.7,0.22,
    Water Distribution,,,Sulfonamides,f,1.8,0.16,
    Water Distribution,,,Sulfonamides,f,1.9,0.11,
    Water Distribution,,,Sulfonamides,f,2.0,0.07,
    Water Distribution,,,Sulfonamides,f,2.1,0.04,
    Water Distribution,,,Sulfonamides,f,2.2,0.02,
    Water Distribution,,,Sulfonamides,f,2.3,0.01,
    Water Distribution,,,Sulfonamides,f,2.4,0.005,
    Water Distribution,,,Sulfonamides,f,2.5,0.002,
    Water Distribution,,,Sulfonamides,f,2.6,0.001,
    Water Distribution,,,Sulfonamides,f,2.7,0.000,
    Water Distribution,,,Tetracyclines,f,0.0,0.32,
    """

    # read_csv 可以直接读取文件路径，也可以读取文件对象
    csv_file_like = StringIO(csv)

    # Pandas 自动解析分隔符和列名
    df = pd.read_csv(csv_file_like, encoding='utf-8')

    # 将 DataFrame 写入 Excel 文件
    excel_filename = "output_data.xlsx"
    sheet_name = "DataSheet"

    # 使用 to_excel 方法写入
    # index=False: 不将 DataFrame 的行索引写入 Excel
    df.to_excel(
        excel_writer=excel_filename,
        sheet_name=sheet_name,
        index=False,
        engine='openpyxl'  # 明确指定写入引擎
    )

    print(f"成功将 CSV 字符串写入到 Excel 文件: {os.path.abspath(excel_filename)}")

    # 打印 DataFrame 以确认数据结构正确
    print("\nDataFrame 预览:")
    print(df)


if __name__ == '__main__':
    csv_to_excel()
