
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
    def minInsertions(self, num: str, k: int) -> str:
        # begin
        # from collections import Counter
        # from functools import lru_cache

        # from itertools import combinations
        # from math import inf
        # from functools import cached_property
        from sortedcontainers import SortedList

        n = len(num)
        gt_cnt = [0] * n  # greater than
        sl = SortedList()
        for i, v in enumerate(num):
            index = sl.bisect_right((v, i))
            gt_cnt[i] = i - index
            sl.add((v, i))

        print(f"input: {num}")
        def log():
            s0 = set(res)
            print("".join(num[j] for j in res) + " " + "".join(num[j] for j in range(n) if j not in s0), k)

        # 子问题
        def dp(s: str, k: int) -> int:
            pass

        res = []
        for loop, (_, i) in enumerate(sl):
            if k <= 0:
                break
            cost = gt_cnt[i]
            if k >= cost:
                res.append(i)
                k -= cost
                log()
            else:
                s0 = set(res)
                for j in range(loop + 1, n):
                    _, i1 = sl[j]
                    if i1 < i and i1 not in s0:
                        cost = gt_cnt[i1]
                        if k >= cost:
                            res.append(i1)
                            k -= cost
                            log()
                break

        s0 = set(res)
        for j in range(n):
            if j not in s0:
                res.append(j)
                if k > 0 and j == i:
                    for _ in range(k):
                        res[j], res[j - 1] = res[j - 1], res[j]
                        j = j - 1
        return "".join(num[j] for j in res)
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
# print(f("4321", 4))  # 1342
# print(f("100", 1))
# print(f("36789", 1000))
print(f("294984148179", 11))  # 124498948179