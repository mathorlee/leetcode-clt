
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
    def calculate_cuts(self, nums: list[int]) -> int:
        # begin
        # from collections import Counter
        # from functools import lru_cache
        # from itertools import combinations
        # from math import inf
        from bisect import bisect_left

        def get_max_ascending_length(nums: list[int]) -> list[int]:
            arr = []
            max_lengths = [0] * len(nums)
            for i, v in enumerate(nums):
                index = bisect_left(arr, v)
                if index < len(arr):
                    arr[index] = min(arr[index], v)
                else:
                    arr.append(v)
                max_lengths[i] = index + 1
            return max_lengths

        a = get_max_ascending_length(nums)
        b = get_max_ascending_length(nums[::-1])
        n = len(nums)
        max_length = 0
        for i in range(1, n - 1):
            if a[i] > 1 and b[n - 1 - i] > 1:
                max_length = max(max_length, a[i] + b[n - 1 - i] - 1)
        return n - max_length
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))
print(f([1,3,1]))
print(f([2,1,1,5,6,2,3,1]))
