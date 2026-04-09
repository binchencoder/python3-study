import jionlp as jio

if __name__ == "__main__":
    result = jio.parse_time("1999年至今")
    print(result)

    result = jio.parse_time("2024年1月")
    print(result)
