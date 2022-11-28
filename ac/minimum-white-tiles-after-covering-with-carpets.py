
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

from functools import lru_cache


class SectionCut(object):
    def minInsertions(self, floor: str, numCarpets: int, carpetLen: int) -> int:
        # begin
        # from collections import Counter
        from functools import lru_cache

        # from itertools import combinations
        # from math import inf
        # from functools import cached_property

        # solution1: TLE, pass 109/2706, O(n^3)
        # @lru_cache(maxsize=None)
        # def dp(s: str, k: int):
        #     if not s or not k:
        #         return 0
        #     if s[0] == "1":
        #         return max(
        #             dp(s[carpetLen:], k - 1) + sum(_ == "1" for _ in s[:carpetLen]),
        #             dp(s[1:], k)
        #         )
        #     else:
        #         index = s.find("1")
        #         if index == -1:
        #             return 0
        #         return dp(s[index:], k)
        # return sum(_ == "1" for _ in floor) - dp(floor, numCarpets)

        # solution2: TLE, pass 204/2706, O(n^2)
        import sys
        sys.setrecursionlimit(2000000)

        n = len(floor)
        pre_sums = [0] * (n + 1)
        for i, c in enumerate(floor):
            pre_sums[i + 1] = pre_sums[i] + (c == "1")

        @lru_cache(maxsize=None)
        def dp(n, k):
            """
            dp[n,k]: 前n个用k个地毯覆盖，最多能覆盖多少个white floor(1)
            dp[n,k] = max(dp[n - carpetLen][k - 1] + sum(1 in floor[n - carpetLen:n]), dp[n - 1,k])
            """
            if k == 0 or n <= 0:
                return 0

            # full cover, the most import optimization. TLE -> runtime_percentile: 94%
            if k >= pre_sums[n] or k * carpetLen >= n:
                return pre_sums[n]

            i = max(n - carpetLen, 0)
            return max(
                dp(i, k - 1) + pre_sums[n] - pre_sums[i],
                dp(n - 1, k)
            )
        return pre_sums[-1] - dp(len(floor), numCarpets)

        # solution

        # n = len(floor)
        # dp = [[0] * (numCarpets + 1) for _ in range(n + 1)]
        # pre_sums = [0] * (n + 1)
        # for i, c in enumerate(floor):
        #     pre_sums[i + 1] = pre_sums[i] + (c == "1")

        # for i in range(1, n + 1):
        #     ii = max(i - carpetLen, 0)
        #     for j in range(1, numCarpets + 1):
        #         dp[i][j] = max(
        #             dp[ii][j - 1] + pre_sums[i] - pre_sums[ii],
        #             dp[i - 1][j]
        #         )
        # return sum(_ == "1" for _ in floor) - dp[n][numCarpets]

        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
print(f("10110101", 2, 2))
print(f("11111", 2, 3))
print(f("0000", 1, 1))
print(f("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111", 28, 31))