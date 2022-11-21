
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
    def calculate_cuts(self, intervals: list[list[int]], queries: list[int]) -> list[int]:
        # begin
        # from collections import Counter
        # from functools import lru_cache
        # from itertools import combinations
        # from math import inf
        from functools import cached_property

        inf = 10 ** 9

        class Node(object):
            def __init__(self, l: int, r: int, v: int = inf) -> None:
                self.l = l
                self.r = r
                self.v = v
                self._lft_child = None
                self._rgt_child = None

            @cached_property
            def mid(self) -> int:
                return (self.l + self.r) >> 1

            @cached_property
            def lft_child(self):
                if not self._lft_child:
                    self._lft_child = Node(self.l, self.mid, self.v)
                return self._lft_child

            @cached_property
            def rgt_child(self):
                if not self._rgt_child:
                    self._rgt_child = Node(self.mid + 1, self.r, self.v)
                return self._rgt_child

            def add(self, l: int, r: int, v: int):
                if v >= self.v:
                    return

                if l == self.l and r == self.r:
                    self.v = v
                    return

                if r <= self.mid:
                    self.lft_child.add(l, r, v)
                elif l >= self.mid + 1:
                    self.rgt_child.add(l, r, v)
                else:
                    self.lft_child.add(l, self.mid, v)
                    self.rgt_child.add(self.mid + 1, r, v)

            def query(self, x) -> int:
                if not self._lft_child and not self._rgt_child:
                    return self.v

                if x <= self.mid:
                    if not self._lft_child:
                        return self.v
                    return min(self.v, self._lft_child.query(x))
                if x > self.mid:
                    if not self._rgt_child:
                        return self.v
                    return min(self.v, self._rgt_child.query(x))
                return inf

        # intervals.sort(key=lambda _: _[1] - _[0] + 1)
        L = min(_[0] for _ in intervals)
        R = max(_[1] for _ in intervals)
        root = Node(L, R)

        # def dfs(node: Node, level: int):
        #     print("   " * level + f"{node.l},{node.r},{node.v}")
        #     if node._lft_child:
        #         dfs(node._lft_child, level + 1)
        #     if node._rgt_child:
        #         dfs(node._rgt_child, level + 1)
        # dfs(root, 0)

        for _ in set(tuple(_) for _ in intervals):
            root.add(_[0], _[1], _[1] - _[0] + 1)
        # print("add complete")
        # dfs(root, 0)

        memo = {}
        res = [-1] * len(queries)
        for i, x in enumerate(queries):
            if L <= x <= R:
                if x in memo:
                    res[i] = memo[x]
                else:
                    v = root.query(x)
                    if v < inf:
                        res[i] = v
                    memo[x] = res[i]

        # print("query complete")
        return res
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))
# print(f([[1,4],[2,4],[3,6],[4,4]], [2,3,4,5]))
# print(f([[2,3],[2,5],[1,8],[20,25]], [2,19,5,22]))
