class DictUtils:
    @staticmethod
    def insert_after(d, after_key, new_dict):
        """在指定键后插入"""
        new_d = {}
        inserted = False
        for k, v in d.items():
            new_d[k] = v
            if k == after_key and not inserted:
                new_d.update(new_dict)
                inserted = True
        if not inserted:
            new_d.update(new_dict)
        return new_d

    @staticmethod
    def insert_before(d, before_key, new_dict):
        """在指定键前插入"""
        new_d = {}
        inserted = False
        for k, v in d.items():
            if k == before_key and not inserted:
                new_d.update(new_dict)
                inserted = True
            new_d[k] = v
        if not inserted:
            new_d.update(new_dict)
        return new_d

    @staticmethod
    def insert_at_index(d, index, new_dict):
        """在指定索引插入"""
        keys = list(d.keys())
        values = list(d.values())

        # 分割
        before_keys = keys[:index]
        after_keys = keys[index:]
        before_values = values[:index]
        after_values = values[index:]

        # 重建
        result = {}
        for i in range(len(before_keys)):
            result[before_keys[i]] = before_values[i]
        result.update(new_dict)
        for i in range(len(after_keys)):
            result[after_keys[i]] = after_values[i]

        return result


if __name__ == '__main__':
    # 使用示例
    original = {'a': 1, 'b': 2, 'c': 3}

    # 在键'b'后插入
    result = DictUtils.insert_after(original, 'b', {'x': 10})
    print(result)  # {'a': 1, 'b': 2, 'x': 10, 'c': 3}
