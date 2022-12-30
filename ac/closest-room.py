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

    def calculate_cuts(self, rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
        # begin
        from dataclasses import dataclass

        from sortedcontainers import SortedList

        @dataclass
        class Room(object):
            no: int
            size: int

        @dataclass
        class Query(object):
            index: int
            preferred: int
            min_size: int

        rs = [Room(no=no, size=size) for no, size in rooms]
        rs.sort(key=lambda _: _.size)
        qs = [Query(index=i, preferred=preferred, min_size=min_size) for i, (preferred, min_size) in enumerate(queries)]
        qs.sort(key=lambda _: _.min_size, reverse=True)

        ret = [-1] * len(qs)
        no_list = SortedList()
        for q in qs:
            while rs and rs[-1].size >= q.min_size:
                no_list.add(rs.pop().no)
            if no_list:
                index = min(no_list.bisect_left(q.preferred), len(no_list) - 1)
                ret[q.index] = no_list[index]
                if index > 0 and abs(no_list[index - 1] - q.preferred) <= abs(no_list[index] - q.preferred):
                    ret[q.index] = no_list[index - 1]
        return ret
        # end

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))  # 210
print(f(rooms=[[2,2],[1,2],[3,2]], queries=[[3,1],[3,3],[5,2]]))  # [3,-1,3]
print(f(rooms=[[1,4],[2,3],[3,5],[4,1],[5,2]], queries=[[2,3],[2,4],[2,5]]))  # [2,1,3]