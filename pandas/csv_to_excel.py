import pandas as pd
import os
from io import StringIO


def csv_to_excel():
    csv = """
    Figure,Year,Region,Legend,Indicator,X,Y,Unit
    Comparison of Soil P Thresholds across Regions,,Northwest,Agronomic soil P threshold of maize and wheat,Soil available P,Northwest,25,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Northwest,Agronomic soil P threshold of rice,Soil available P,Northwest,22,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Northwest,Environmental soil P threshold,Soil available P,Northwest,40,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Northeast,Agronomic soil P threshold of maize and wheat,Soil available P,Northeast,19,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Northeast,Agronomic soil P threshold of rice,Soil available P,Northeast,23,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Northeast,Environmental soil P threshold,Soil available P,Northeast,52,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Central China,Agronomic soil P threshold of maize and wheat,Soil available P,Central China,25,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Central China,Agronomic soil P threshold of rice,Soil available P,Central China,20,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Central China,Environmental soil P threshold,Soil available P,Central China,52,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Yangtze Plain,Agronomic soil P threshold of maize and wheat,Soil available P,Yangtze Plain,27,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Yangtze Plain,Agronomic soil P threshold of rice,Soil available P,Yangtze Plain,19,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,Yangtze Plain,Environmental soil P threshold,Soil available P,Yangtze Plain,40,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,South China,Agronomic soil P threshold of maize and wheat,Soil available P,South China,25,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,South China,Agronomic soil P threshold of rice,Soil available P,South China,25,mg kg^-1
    Comparison of Soil P Thresholds across Regions,,South China,Environmental soil P threshold,Soil available P,South China,50,mg kg^-1
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
