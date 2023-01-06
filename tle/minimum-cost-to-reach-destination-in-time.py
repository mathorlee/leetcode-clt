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

    def calculate_cuts(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        # begin
        from collections import defaultdict, deque
        from functools import cache
        from sortedcontainers import SortedList, SortedDict
        import sys
        sys.setrecursionlimit(10**6)

        n = len(passingFees)
        inf = float("inf")

        time_d = {}
        def add_time(a, b, time):
            if a > b:
                a, b = b, a
            time_d[a, b] = min(time_d.get((min(a, b), max(a, b)), inf), time)

        def get_time(a, b):
            return time_d.get((min(a, b), max(a, b)), inf)

        for a, b, time in edges:
            add_time(a, b, time)

        edge_d = defaultdict(list)
        for (a, b), time in time_d.items():
            # print(a, b, time)
            edge_d[a].append(b)
            edge_d[b].append(a)
        
        # Solution 2，利用收敛特性，TLE，pass 79/92
        # res = [[] for _ in range(n)]  # res[i] = [(time, fee), ...]
        # def add(node, time, fee):
        #     for _ in res[node]:
        #         if _[0] <= time and _[1] <= fee:
        #             return False
        #     res[node].append((time, fee))
        #     return True

        # Solution 3
        # res = [SortedDict() for _ in range(n)]  # res[i] = [(time, fee), ...]
        # def add(node, time, fee):
        #     d = res[node]
        #     index = d.bisect_left(time)
        #     if index > 0:
        #         pre_time, pre_fee = d.peekitem(index - 1)
        #         if pre_time <= time and pre_fee <= fee:
        #             return False
        #     while index < len(d):
        #         nxt_time, nxt_fee = d.peekitem(index)
        #         if time <= nxt_time and fee < nxt_fee:
        #             d.pop(nxt_time)
        #         else:
        #             break
        #     d[time] = fee
        #     return True

        # add(0, 0, passingFees[0])
        # q = deque([(0, 0, passingFees[0])])
        # while q:
        #     node, time, fee = q.popleft()
        #     for neighbor in edge_d[node]:
        #         _ = get_time(node, neighbor)
        #         new_time = time + get_time(node, neighbor)
        #         if new_time <= maxTime:
        #             new_fee = fee + passingFees[neighbor]
        #             if add(neighbor, new_time, new_fee):
        #                 q.append((neighbor, new_time, new_fee))
        # # for i, _ in enumerate(res):
        # #     print(i, dict(_))
        # if not res[-1]:
        #     return -1
        # return min(res[-1].values())

        # Solution 1: TLE, pass 49/92
        @cache
        def dp(max_time, node):
            if max_time < 0:
                return inf
            if node == 0:
                return passingFees[node]

            res = inf
            for neighbor in edge_d[node]:
                time = get_time(node, neighbor)
                res = min(res, dp(max_time - time, neighbor) + passingFees[node])
            return res
        res = dp(maxTime, n - 1)
        if res == inf:
            return -1
        return res
        # end

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))  # 364109
print(f(boxes=[[1,1],[2,1],[1,1]], portsCount=2, maxBoxes=3, maxWeight=3))  # 4
print(f(boxes=[[1,2],[3,3],[3,1],[3,1],[2,4]], portsCount=3, maxBoxes=3, maxWeight=6))  # 6
print(f(boxes=[[1,4],[1,2],[2,1],[2,1],[3,2],[3,4]], portsCount=3, maxBoxes=6, maxWeight=7))  # 6