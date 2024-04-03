def str_format(key):
    return "{}_{}".format("pie-gpt", key)


def str_f(key):
    return f"pie-gpt_{key}"


if __name__ == "__main__":
    print(str_format("aaa"))
    print(str_f("aaa"))
