
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
    def calculate_cuts(self, nums: list[int], k: int) -> int:
        # begin
        from collections import defaultdict
        from functools import lru_cache
        from itertools import combinations
        from math import inf

        # illegal case
        d = defaultdict(int)
        for _ in nums:
            d[_] += 1
            if d[_] > k:
                return -1

        # general casese
        n, m = len(nums), len(nums) // k
        d = {}  # d[mask] = (max_num - min_num) and mask has m one bit.
        for indices in combinations(range(n), m):
            mask = 0
            s = set()
            for _ in indices:
                mask |= (1 << _)
                s.add(nums[_])
            if len(s) == m:
                d[mask] = max(s) - min(s)

        @lru_cache(maxsize=None)
        def dfs(mask: int) -> int:
            res = inf
            if mask in d:
                return d[mask]

            for sub_mask in d:
                if mask & sub_mask == sub_mask:
                    res = min(res, d[sub_mask] + dfs(mask ^ sub_mask))

            return res  # type: ignore

        res = dfs((1 << n) - 1)
        return res if res < inf else -1

        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))
print(f([1,2,1,4], 2))
print(f([6,3,8,1,3,1,2,2], 4))
print(f([5,3,3,6,3,3], 3))
print(f([7,3,16,15,1,13,1,2,14,5,3,10,6,2,7,15], 8))
