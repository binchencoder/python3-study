import clevercsv
import csv

if __name__ == "__main__":
    # df = clevercsv.read_dataframe(
    #     "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/领域知识/海/法国海军.csv",
    #     # "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/武器库/05雷达/PDF表格到Excel文件.csv",
    #     delimiter=",",
    #     quotechar="",
    #     escapechar="\\",
    # )
    # print(df)

    # with open(
    #     "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/领域知识/海/法国海军.csv",
    #     # "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/武器库/05雷达/PDF表格到Excel文件.csv",
    #     "r",
    #     newline="",
    # ) as csvfile:
    #     # you can use verbose=True to see what CleverCSV does
    #     dialect = clevercsv.Sniffer().sniff(csvfile.read(), verbose=False)
    #     csvfile.seek(0)
    #     reader = clevercsv.reader(csvfile, dialect)
    #     rows = list(reader)
    #     print(rows)

    dialect = clevercsv.detect_dialect(
        "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/武器库/05雷达/PDF表格到Excel文件.csv",
        # "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/领域知识/海/法国海军.csv",
    )
    with open(
        "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/武器库/05雷达/PDF表格到Excel文件.csv",
        # "/home/chenbin/workspace/PIE-Knowledge/数据工程/朱总提供/领域知识/海/法国海军.csv",
        newline="",
    ) as csvfile:
        reader = csv.reader(csvfile, dialect=dialect, quotechar=",", escapechar="\\")
        for row in reader:
            print(row)
