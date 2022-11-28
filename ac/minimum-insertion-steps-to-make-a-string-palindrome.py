
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
    def minInsertions(self, s: str) -> int:
        # begin
        # from collections import Counter
        from functools import lru_cache
        # from itertools import combinations
        # from math import inf
        # from functools import cached_property

        @lru_cache(maxsize=None)
        def dp(s):
            if len(s) <= 1:
                return 0
            if s[0] == s[-1]:
                return dp(s[1:-1])
            return min(dp(s[1:]), dp(s[:-1])) + 1
        return dp(s)
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
# print(f("aabb"))
# print(f("letelt"))
# print(f("abbcdeaedcbb"))
# print(f("zzazz"))
# print(f("mbadm"))
# print(f("leetcode"))
print(f("tldjbqjdogipebqsohdypcxjqkrqltpgviqtqz"))