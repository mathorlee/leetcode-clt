def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

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


def k_array(s):
    ret = [0] * len(s)
    for i in range(1, len(s)):
        j = ret[i - 1]
        while j > 0 and s[i] != s[j]:
            j = ret[j - 1]
        if s[i] == s[j]:
            j += 1
        ret[i] = j
    return ret


class SectionCut(object):
    def minInsertions(self, nums: list[int]):
        # begin
        from sortedcontainers import SortedList

        n = len(nums)
        res = [-1] * n
        greater_count = [0] * n

        sl = SortedList()
        sl.add((nums[0], 0))

        for i in range(1, n):
            v = nums[i]
            index = sl.bisect_left((v, 0))
            for j in range(index - 1, -1, -1):
                _ = sl[j][1]
                greater_count[_] += 1
                if greater_count[_] == 2:
                    res[_] = v
                    sl.pop(j)
            sl.add((v, i))
        return res
        # end

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
print(f(nums=[2,4,0,9,6]))  # [9,6,6,-1,-1]
print(f(nums=[3,3]))  # [-1,-1]