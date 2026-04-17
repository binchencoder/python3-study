from itertools import combinations


def all_groupings_fixed_size(strings, group_size=2):
    """
    穷举所有可能的分组情况，每个组有固定数量的元素
    使用规范化方法避免重复
    """
    unique_strings = list(dict.fromkeys(strings))
    n = len(unique_strings)

    if n == 0:
        return [[]]

    all_results = []

    def backtrack(remaining, current_groups):
        if not remaining:
            # 规范化分组：对每组排序，然后对分组列表排序
            normalized_groups = []
            for group in current_groups:
                normalized_groups.append(tuple(sorted(group)))
            normalized_groups.sort()
            all_results.append([list(group) for group in normalized_groups])
            return

        current_group_size = min(group_size, len(remaining))

        # 为了去重，我们只从剩余元素中选择第一个元素所在的组
        first_element = remaining[0]

        # 从剩余元素中选择current_group_size-1个其他元素
        for others in combinations([e for e in remaining if e != first_element], current_group_size - 1):
            new_group = [first_element] + list(others)
            # 更新剩余元素
            new_remaining = [e for e in remaining if e not in new_group]
            backtrack(new_remaining, current_groups + [new_group])

    backtrack(unique_strings, [])

    # 再次去重（以防万一）
    unique_results = []
    seen = set()
    for grouping in all_results:
        # 将分组转换为可哈希的形式
        grouping_tuple = tuple(tuple(sorted(group)) for group in grouping)
        if grouping_tuple not in seen:
            seen.add(grouping_tuple)
            unique_results.append(grouping)

    return unique_results


def print_all_groupings_directly(strings, group_size=2):
    """
    直接打印所有分组情况，不带方案编号
    """
    results = all_groupings_fixed_size(strings, group_size)

    for grouping in results:
        # 格式化每个分组：用括号包围每个组，用竖线分隔
        formatted = " | ".join([f"({', '.join(group)})" for group in grouping])
        print(formatted)


def pairwise_combinations(arr, chunk_size=2):
    return [list(pair) for pair in combinations(arr, chunk_size)]


# 方法二：手写双重循环（不依赖库）
def pairwise_combinations_manual(arr):
    result = []
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            result.append([arr[i], arr[j]])
    return result


if __name__ == '__main__':
    # 测试
    strings = ["老鸭头", "个股异动", "九转序列", "缺口突破"]

    print("pairwise_combinations: 4个元素，每组2个：")
    print(pairwise_combinations(strings, 2))

    print("\npairwise_combinations: 4个元素，每组3个：")
    print(pairwise_combinations(strings, 3))

    # print("=== 测试1：4个元素，每组2个 ===")
    # print_all_groupings_directly(strings, 2)
    #
    # print("\n=== 测试2：4个元素，每组3个 ===")
    # print_all_groupings_directly(strings, 3)

    print("\n4个元素，每组2个：")
    print_all_groupings_directly(["A", "B", "C", "D"], 2)

    print("\n6个元素，每组3个：")
    print_all_groupings_directly(["A", "B", "C", "D", "E", "F"], 3)

    print("\n5个元素，每组2个：")
    print_all_groupings_directly(["A", "B", "C", "D", "E"], 2)
