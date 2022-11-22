
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
    def calculate_cuts(self, s: str) -> int:
        # begin
        # from collections import Counter
        # from functools import lru_cache
        # from itertools import combinations
        # from math import inf
        # from functools import cached_property
        arr = [_ for _ in s]
        n = len(arr)
        i, j = 0, n -1
        res = 0
        while s:
            # print(s, res)
            if len(s) == 1 or (len(s) == 2 and s[0] == s[1]):
                break
            if s[0] == s[-1]:
                s = s[1:-1]
            else:
                i = len(s) - 1
                while s[i] != s[0]:
                    i -= 1
                if i == 0:
                    res += (len(s) - 1) // 2
                else:
                    res += len(s) - 1 - i
                s = s[1:i] + s[i + 1:]

        return res
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))
# print(f("aabb"))
# print(f("letelt"))
# print(f("abbcdeaedcbb"))
print(f("skwhhaaunskegmdtutlgtteunmuuludii"))  # 163