
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

def mask_to_digit(mask: int):
    import math
    while mask:
        i = mask & -mask
        yield int(math.log2(i))
        mask = mask ^ i
    yield from ()


class SectionCut(object):
    def calculate_cuts(self, packages: list[int], boxes: list[list[int]]) -> int:
        # begin
        from bisect import bisect_right
        from math import inf

        n = len(packages)
        packages.sort()

        def cal_waste(box: list[int]):
            res = 0
            i = 0
            for v in box:
                j = bisect_right(packages, v)
                if j > i:
                    res += (j - i) * v
                i = j
                if i >= n:
                    break
            return inf if i < n else res

        res = inf
        for _ in boxes:
            _.sort()
            res = min(cal_waste(_), res)
        return -1 if res == inf else (res - sum(packages)) % (10**9 + 7)
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().calculate_cuts
# print(f([2,3,5], boxes=[[4,8],[2,8]]))
# print(f([2,3,5], boxes=[[1,4],[2,3],[3,4]]))
# print(f([3,5,8,10,11,12], boxes=[[12],[11,9],[10,5,14]]))
input = read_input()
print(f(*input))
# print(f(list(range(1, 100001)), [[72362, 100000]]))
# print(f(list(range(1, 11)), [[7, 10]]))
print(f([2,3,5],[[1,4],[2,3],[3,4]]))