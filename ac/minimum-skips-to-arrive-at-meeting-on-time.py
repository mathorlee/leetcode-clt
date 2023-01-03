import math
from typing import Dict, List


def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]


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

    def calculate_cuts(self, dist: List[int], speed: int, hoursBefore: int) -> int:
        # begin
        """
        dp[n][k] = min(ceil(dp[n - 1][k]) + dist[n]/speed, dp[n - 1][k - 1] + dist[n] / speed)
        """
        import math
        from functools import cache
        import sys
        sys.setrecursionlimit(10**6)

        if sum(dist) // speed > hoursBefore:
            return -1

        n = len(dist)

        @cache
        def dp(n, k):
            if k == 0:  # 不跳过
                return sum(math.ceil(dist[i] / speed) for i in range(n)) + dist[n] / speed
            if n == 0:
                return dist[n] / speed
            x = dp(n - 1, k)
            y = math.ceil(x)
            if abs(y - x - 1) < 1e-8:  # 处理该死的浮点数相等问题
                y -= 1
            return min(y, dp(n - 1, k - 1)) + dist[n] / speed

        # print(n, hoursBefore)
        for k in range(n):
            # print(n - 1, k, dp(n - 1, k))
            if dp(n - 1, k) <= hoursBefore:
                return k
        return -1
        # end

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))  # 665
# print(f(dist=[1,3,2], speed=4, hoursBefore=2))  # 1
# print(f(dist=[7,3,5,5], speed=2, hoursBefore=10))  # 2
# print(f(dist=[7,3,5,5], speed=1, hoursBefore=10))  # -1