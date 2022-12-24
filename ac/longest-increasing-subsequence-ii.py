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

def get_primes(N):
    # N=round(N) + 1
    N = N + 1
    is_prime = [True] * N
    for i in range(2, N):
        if is_prime[i]:
            j = i * 2
            while j < N:
                is_prime[j] = False
                j += i
    return [_ for _ in range(2, N) if is_prime[_]]

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
    def calculate_cuts2(self, vals: list[int], edges: list[list[int]]) -> int:
        """
        根节点->子节点的路径上的所有节点的val是非降序的，找到所有这样的子节点，按照子树和val分组
        """
        from collections import defaultdict

        edge_d = defaultdict(list)
        for a, b in edges:
            edge_d[a].append(b)
            edge_d[b].append(a)
        visisted = set()

        self.res = 0
        def dfs(root: int, depth):
            """return {val: count} Count(_.val for _ in root if root -> _ is non descending on val)"""
            print(" " * depth * 4 + f"({vals[root]})")
            visisted.add(root)
            d = defaultdict(int)
            for i, child in enumerate(edge_d[root]):
                if child not in visisted:
                    child_d = dfs(child, depth + 1)
                    if vals[child] <= vals[root]:
                        for val, count in child_d.items():
                            d[val, i] += count

            new_d = defaultdict(list)
            for (val, _), count in d.items():
                new_d[val].append(count)
            for val, counts in new_d.items():
                for i in range(len(counts)):
                    for j in range(i + 1, len(counts)):
                        self.res += counts[i] * counts[j]
                if val == vals[root]:
                    self.res += sum(counts)

            new_d = {val: sum(counts) for val, counts in new_d.items()}
            new_d[vals[root]] = new_d.get(vals[root], 0) + 1
            return new_d

        dfs(0, 0)
        return self.res + len(vals)

    def calculate_cuts(self, nums: list[int], k: int) -> int:
        # begin
        """
        sorteddict, 以k为end的合法子序列的最大长度
        """
        from dataclasses import dataclass
        from functools import cached_property
        from typing import Optional

        @dataclass
        class STNode(object):
            lo: int
            hi: int
            metric: int = 0
            left_child: Optional["STNode"] = None
            right_child: Optional["STNode"] = None

            @cached_property
            def mid(self) -> int:
                return (self.lo + self.hi) >> 1

            def build(self):
                if self.lo == self.hi:
                    return

                if not self.left_child:
                    self.left_child = STNode(lo=self.lo, hi=self.mid, metric=self.metric)
                    self.left_child.build()
                if not self.right_child:
                    self.right_child = STNode(lo=self.mid + 1, hi=self.hi, metric=self.metric)
                    self.right_child.build()

            def update(self, k, v):
                self.metric = max(self.metric, v)
                if self.lo == self.hi == k:
                    return
                if k > self.mid:
                    self.right_child.update(k, v)
                else:
                    self.left_child.update(k, v)

            def query(self, lo, hi) -> int:
                if lo == self.lo and hi == self.hi:
                    return self.metric
                if lo > self.mid:
                    return self.right_child.query(lo, hi)
                if hi <= self.mid:
                    return self.left_child.query(lo, hi)
                return max(
                    self.left_child.query(lo, self.mid),
                    self.right_child.query(self.mid + 1, hi),
                )

        res = 0
        t = STNode(lo=min(nums), hi=max(nums))
        t.build()
        for _ in nums:
            lo, hi = max(t.lo, _ - k), _ - 1
            v = t.query(lo, hi) if lo <= hi else 0
            t.update(_, v + 1)
            res = max(res, v + 1)
        return res
        # end

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))  # [1,1,2,2,2,2,2,2,2,1]
print(f(nums=[4,2,1,4,3,4,5,8,15], k=3))  # 5
print(f(nums=[7,4,5,1,8,12,4,7], k=5))  # 4
print(f(nums=[1,5], k=1))  # 1
