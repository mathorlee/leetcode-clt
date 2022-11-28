
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


class SectionCut(object):
    def calculate_cuts(self, n: int, cuts: list[int]) -> int:
        # begin
        # import itertools as it
        # import math
        from functools import lru_cache
        cuts.extend((0, n))
        cuts.sort()

        @lru_cache(maxsize=None)
        def dfs(i, j) -> int:
            if i + 1 == j:
                return 0

            res = 10**9
            for k in range(i + 1, j):
                res = min(res, cuts[j] - cuts[i] + dfs(i, k) + dfs(k, j))
            return res

        return dfs(0, len(cuts) - 1)
        # end

f = SectionCut().calculate_cuts
print(f(7, [1,3,4,5]))
print(f(9, [5,6,1,4,2]))
