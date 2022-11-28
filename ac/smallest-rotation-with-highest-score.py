
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
    def minInsertions(self, nums: list[int]) -> int:
        # begin
        from sortedcontainers import SortedList

        # Solution 1: TLE, pass 27/44, O(n^2)
        # n = len(nums)
        # arr = [v - i for i, v in enumerate(nums)]
        # res = (sum(_ <= 0 for _ in arr), 0)
        # for k in range(1, n):
        #     arr.pop(0)
        #     arr.append(nums[k - 1] - (n - 1 + k))
        #     _ = sum(_ <= -k for _ in arr)
        #     if _ > res[0]:
        #         res = (_, k)
        # return res[-1]

        # Solution 2, AC, runtime_percentile: 5.2054999999998675, 6338 ms
        n = len(nums)
        arr = SortedList((v - i, i) for i, v in enumerate(nums))
        res = (arr.bisect_left((1, 0)), 0)
        for k in range(1, n):
            i = k - 1
            v = nums[i]
            arr.remove((v - i, i))
            arr.add((v - (i + n), i))  # index increased by n
            _ = arr.bisect_left((-k + 1, 0))
            if _ > res[0]:
                res = (_, k)
        return res[-1]
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
print(f([2,3,1,4,0]))
print(f([1,3,0,2,4]))