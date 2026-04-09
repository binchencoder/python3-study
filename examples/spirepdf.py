"""
pip install Spire.PDF
"""

from spire.pdf import *
from spire.pdf.common import *
from spire.xls import *


if __name__ == "__main__":
    # 创建PdfDocument类的实例
    # pdf = PdfDocument()

    # # 加载PDF文件
    # pdf.LoadFromFile(
    #     "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/武器库/05雷达/ANTPQ-37炮位侦察雷达.pdf"
    # )

    # # 创建列表
    # list = []

    # # 创建PdfTableExtractor对象
    # extractor = PdfTableExtractor(pdf)

    # # 遍历文档的页面
    # for pageIndex in range(pdf.Pages.Count):
    #     # 从页面提取表格
    #     tableList = extractor.ExtractTable(pageIndex)

    #     # 检查表格列表是否不为空且列表不为空
    #     if tableList is not None and len(tableList) > 0:
    #         # 遍历列表中的表格
    #         for table in tableList:
    #             tableData = ""
    #             # 获取行数和列数
    #             row = table.GetRowCount()
    #             column = table.GetColumnCount()

    #             # 遍历表格的行和列
    #             for i in range(row):
    #                 for j in range(column):
    #                     # 从单元格获取文本
    #                     text = table.GetText(i, j)

    #                     # 将文本添加到列表中
    #                     tableData += text + " "
    #                 tableData += "\n"
    #         list.append(tableData)

    # # 将每个表格保存为txt文件
    # for i in range(len(list)):
    #     fileName = "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/武器库/05雷达/ExtractedPDFTables{0}.txt".format(
    #         i
    #     )
    #     with open(fileName, "w") as f:
    #         f.writelines(list[i])

    # # 释放资源
    # pdf.Close()

    # 创建一个PdfDocument对象
    doc = PdfDocument()

    # 加载示例PDF文件
    doc.LoadFromFile(
        "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/领域知识/海/法国海军.pdf"
    )

    # 创建一个Workbook对象
    workbook = Workbook()

    # 清除默认的工作表
    workbook.Worksheets.Clear()

    # 创建一个PdfTableExtractor对象
    extractor = PdfTableExtractor(doc)

    sheetNumber = 1

    # 循环遍历页面
    for pageIndex in range(doc.Pages.Count):
        # 从特定页面提取表格
        tableList = extractor.ExtractTable(pageIndex)

        # 判断表格列表是否不为空
        if tableList is not None and len(tableList) > 0:
            # 循环遍历列表中的表格
            for table in tableList:
                # 添加一个工作表
                sheet = workbook.Worksheets.Add(f"sheet{sheetNumber}")

                # 获取某个表格的行数和列数
                row = table.GetRowCount()
                column = table.GetColumnCount()

                # 循环遍历行和列
                for i in range(row):
                    for j in range(column):
                        # 从特定单元格获取文本
                        text = table.GetText(i, j)

                        # 将文本写入指定的单元格
                        sheet.Range[i + 1, j + 1].Value = text

                # 自动调整列宽
                sheet.AllocatedRange.AutoFitColumns()

                sheetNumber += 1

    # 保存到文件
    workbook.SaveToFile(
        "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/领域知识/海/法国海军.csv"
    )
    workbook.Dispose()
