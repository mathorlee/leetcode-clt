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
        pass
        # end

from sortedcontainers import SortedList


def range_overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """
    (10, 11), (12, 13), not overlap
    (10, 11), (11, 12), overlap
    """
    arr = sorted(a + b)
    return a[1] - a[0] + b[1] - b[0] >= arr[-1] - arr[0]

def merge_range(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    arr = sorted(a + b)
    return (arr[0], arr[-1])

def get_range_value(a: tuple[int, int]):
    return a[1] - a[0] + 1

class CountIntervals:

    def __init__(self):
        self.arr = SortedList()
        self.v = 0

    def get_range(self, k: int) -> tuple[int, int]:
        return (self.arr[k * 2], self.arr[k * 2 + 1])  # type: ignore

    def delete_range(self, k: int):
        self.arr.pop(2 * k + 1)
        self.arr.pop(2 * k)

    def add(self, left: int, right: int) -> None:
        """
        arr: (1, 10), (11, 12), (15,15) (20, 30)
        add(10, 16)
        add(2, 100)?
        add(100, 101)?
        add(-2, -1)
        """
        a = (left, right)
        i = self.arr.bisect_left(left) // 2
        j = self.arr.bisect_left(right) // 2
        j = min(len(self.arr) // 2 - 1, j)
        for k in range(j, i - 1, -1):
            b = self.get_range(k)
            if range_overlap(a, b):
                a = merge_range(a, b)
                self.v -= get_range_value(b)
                self.delete_range(k)
        self.v += get_range_value(a)
        self.arr.update(a)

    def count(self) -> int:
        return self.v

# f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
# print(f(grid=[["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]))  # true
# print(f(grid=[[")",")"],["(","("]]))  # false

f = CountIntervals()
f.add(2, 3)
f.add(7, 10)
print(f.count())
f.add(5, 8)
print(f.count())
