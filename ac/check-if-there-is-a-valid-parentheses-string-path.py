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
    def minInsertions(self, grid: list[list[str]]) -> bool:
        # begin
        from collections import defaultdict

        m, n = len(grid), len(grid[0])
        v = 0
        d = defaultdict(set)
        for j in range(n):
            if grid[0][j] == "(":
                v += 1
            else:
                v -= 1
            if v >= 0:
                d[j].add(v)
            if v < 0:
                break

        # for _ in grid:
        #     print("".join(_))
        # print(m, n)
        # print(d)
        for i in range(1, m):
            new_d = defaultdict(set)
            for j in range(n):
                s0 = d[j]
                if j:
                    s0 |= new_d[j - 1]  # type: ignore
                for v in s0:
                    if grid[i][j] == "(":
                        v += 1
                    else:
                        v -= 1
                    if v >= 0:
                        new_d[j].add(v)
            d = new_d
            # print(d)
        return 0 in d[n - 1]
        # end

f = SectionCut().minInsertions
input = read_input()
print(f(*input))
# print(f(grid=[["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]))  # true
# print(f(grid=[[")",")"],["(","("]]))  # false