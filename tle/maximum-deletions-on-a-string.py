
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
    def minInsertions(self, s: str) -> int:
        # begin

        from functools import lru_cache
        import sys
        sys.setrecursionlimit(10000)

        # TLE, pass 113/129
        @lru_cache(None)
        def dp(a):
            res = 1
            for i in range(1, (len(s) - a) // 2 + 1):
                if s[a:a + i] == s[a + i:a + 2 * i]:
                    res = max(res, 1 + dp(a + i))
            return res
        return dp(0)

        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
input = read_input()
print(f(*input))
for _ in ("abcabcdabc", "aaabaab", "aaaaa"):
    print(f(_))
