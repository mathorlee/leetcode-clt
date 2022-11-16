
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
    def calculate_cuts(self, tires: list[list[int]], changeTime: int, numLaps: int) -> int:
        # begin
        # import itertools as it
        import math
        from functools import lru_cache

        # get min(x) when a * b**(x - 1) >= a + changeTime
        # x = ceil(log((a + changeTime) / a, b) + 1)
        MAX_X = max(math.ceil(math.log((a + changeTime) / a, b) + 1) for a, b in tires)
        a, b = tires[0]
        MAX_RES = a * b * numLaps + changeTime * (numLaps - 1)

        @lru_cache(maxsize=None)
        def dp(n) -> int:
            res = min(a * (b**n - 1) // (b - 1) for a, b in tires) if n <= MAX_X else MAX_RES
            for i in range(1, min(n // 2, MAX_X) + 1):
                res = min(dp(i) + dp(n - i) + changeTime, res)
            return res

        return dp(numLaps)
        # end

f = SectionCut().calculate_cuts
print(f([[2,3],[3,4]], 5, 4))
print(f([[1,10],[2,2],[3,4]], 6, 5))