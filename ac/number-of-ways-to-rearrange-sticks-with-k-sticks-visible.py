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

    def calculate_cuts(self, n: int, k: int) -> int:
        # begin
        """
        dp[n][k] = dp[n - 1][k - 1] + dp[n - 1][k] * (n - 1)
        dp[n][1] = (n - 1)!
        """
        MOD = 10**9 + 7
        factorials = [1, 1]
        for i in range(2, n):
            factorials.append(factorials[-1] * i % MOD)

        dp = [[0] * (k + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            dp[i][1] = factorials[i - 1]
            if k >= i:
                dp[i][i] = 1

        for i in range(2, n + 1):
            for j in range(2, min(k + 1, i)):
                dp[i][j] = (dp[i - 1][j - 1] + dp[i - 1][j] * (i - 1)) % MOD
        # for _ in dp:
        #     print(_)
        return dp[n][k]
        # end

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))  # 26
print(f(n=3, k=2))  # 3
print(f(n=5, k=5))  # 1
print(f(n=20, k=11))  # 647427950