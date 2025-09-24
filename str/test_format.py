def str_format(key):
    return "{}_{}".format("pie-gpt", key)


def str_f(key):
    return f"pie-gpt_{key}"


def replace_space(text: str):
    # 过滤掉所有的空格
    no_spaces = "".join(char for char in text if char != " ")

    return no_spaces


def substr(text: str):
    return text[:3]


def format_sheetname(sheetname: str) -> str:
    if sheetname is None or sheetname.strip() == "":
        return ""

    return sheetname.replace(" ", "")[:5]


if __name__ == "__main__":
    print(str_format("aaa"))
    print(str_f("aaa"))

    print("a a a bc cc   ccc  ".replace(" ", ""))
    print(replace_space("a a a bc cc   ccc  "))

    print(substr("a a a a bc cc   ccc  "))

    print(format_sheetname("a a a a bc cc   ccc "))
