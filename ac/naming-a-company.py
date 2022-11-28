
def binary_of_int(i: int, width: int) -> str:
    if i >= 0:
        return f"%0{width}d" % int(bin(i)[2:])
    
    # if i < 0, binary(i) = 反码(binary(-i - 1))
    s = ""
    for _ in binary_of_int(-i - 1, width):
        if _ == "1":
            s += "0"
        else:
            s += "1"
    return s

def mask_to_bits(mask: int):
    import math
    while mask:
        i = mask & -mask
        yield int(math.log2(i))
        mask = mask ^ i
    yield from ()


class SectionCut(object):
    def minInsertions(self, ideas: list[str]) -> int:
        # begin
        from collections import defaultdict
        from bisect import bisect_left

        n = len(ideas)

        # Solution 1: brute force TLE, pass 63/89
        # s0 = set()
        # for i in range(n):
        #     for j in range(n):
        #         if i != j:
        #             a, b = ideas[j][0] + ideas[i][1:], ideas[i][0] + ideas[j][1:]
        #             if a not in ideas and b not in ideas:
        #                 # print(ideas[i], ideas[j])
        #                 s0.add(a + b)
        # print(len(s0))

        # Solution2: ideas按照最长后缀[1:]分组，最多有9!=362880个不同的后缀。TLE, pass 75/89
        # d =defaultdict(set)
        # for _ in ideas:
        #     d[_[1:]].add(_[0])
        # arr = list(d.values())
        # res = 0
        # for i in range(len(arr)):
        #     for j in range(i + 1, len(arr)):
        #         common_prefix_count = len(arr[i].intersection(arr[j]))
        #         res += (len(arr[i]) - common_prefix_count) * (len(arr[j]) - common_prefix_count)
        # return res * 2

        # Solution 3
        d =defaultdict(set)
        for _ in ideas:
            d[_[0]].add(_[1:])
        res = 0
        for k, v in d.items():
            for k1, v1 in d.items():
                if k < k1:
                    same_cnt = len(v & v1)
                    res += (len(v) - same_cnt) * (len(v1) - same_cnt)
        return res * 2
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
print(f(["coffee","donuts","time","toffee"]))
print(f(["lack","back"]))
print(f(["aaa","baa","caa","bbb","cbb","dbb"]))  # 2