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

    def calculate_cuts(self, n: int, restrictions: List[List[int]]) -> int:
        # begin
        from dataclasses import dataclass

        from sortedcontainers import SortedList

        if len(restrictions) == 0:
            return n - 1

        @dataclass
        class Restriction(object):
            index: int
            height: int  # 限高
            pre_r: "Restriction" = None
            next_r: "Restriction" = None

            def pull_down_height_by_other(self, other: "Restriction"):
                """被other把限高拉低"""
                if other.height < self.height:
                    _ = self.height - other.height - abs(self.index - other.index)
                    if _ > 0:
                        self.height -= _

            def get_max_height(self, other: "Restriction"):
                _ = abs(self.height - other.height) - abs(self.index - other.index)
                res = max(self.height, other.height)
                if _ < 0:
                    res += abs(_) // 2
                return res

        rs = [Restriction(index=index - 1, height=min(index - 1, height)) for index, height in restrictions]
        d = {_.index: _ for _ in rs}
        rs.sort(key=lambda _: _.index)
        m = len(rs)
        for i in range(m):
            if i > 0:
                rs[i].pre_r = rs[i - 1]
                rs[i - 1].next_r = rs[i]

        arr = SortedList((_.height, _.index) for _ in rs)
        for i in range(m):
            r = d[arr[i][1]]
            for o in (r.pre_r, r.next_r):
                if o:
                    _ = o.height
                    o.pull_down_height_by_other(r)
                    if _ != o.height:
                        arr.remove((_, o.index))
                        arr.add((o.height, o.index))

        # 获取结果
        res = rs[0].get_max_height(Restriction(index=-1, height=-1))  # 构造一个索引为-1的restriction
        for i in range(1, m):  # [(0, 1), ..., (n - 2, n - 1)]
            res = max(res, rs[i].get_max_height(rs[i - 1]))
        res = max(res, rs[-1].height + n - 1 - rs[-1].index)  # 最后一个
        return res
        # end

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))  # 1
# print(f(n=5, restrictions=[[2,1],[4,1]]))  # 2
# print(f(n=6, restrictions=[]))  # 5
# print(f(n=10, restrictions=[[5,3],[2,5],[7,4],[10,3]]))  # 5