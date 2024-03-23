def main():
    s = [1, 2, 3, 4, 5]
    e = enumerate(s)
    for i, v in e:
        print(f"index: {i}, value: {v}")


if __name__ == "__main__":
    main()
