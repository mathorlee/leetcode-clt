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

    def calculate_cuts(self, colors: str, edges: List[List[int]]) -> int:
        # begin
        from collections import defaultdict, deque

        n = len(colors)
        indgree_d = defaultdict(int)
        edge_d = defaultdict(list)
        for a, b in edges:
            edge_d[a].append(b)
            indgree_d[b] += 1

        # Solution 2: bfs + 拓扑排序，太秀了
        counts = [defaultdict(int) for _ in range(n)]  # counts[i] = {"a": 1, ...}, counts[i]表示nodes[i]为终点的path的每个颜色的最大数量
        q = deque(_ for _ in range(n) if indgree_d[_] == 0)
        while q:
            u = q.popleft()
            color = colors[u]
            counts[u][color] += 1
            for v in edge_d[u]:
                for i, j in counts[u].items():
                    counts[v][i] = max(counts[v][i], j)
                indgree_d[v] -= 1
                if indgree_d[v] == 0:
                    q.append(v)

        if any(indgree_d[_] > 0 for _ in range(n)):
            return -1

        res = 0
        for _ in counts:
            for v in _.values():
                res = max(res, v)
        return res

        # Solution 1: DFS, TLE pass 40/83
        # visisted = set()
        # color_d = defaultdict(int)
        # color_counts = SortedList((0, color) for color in set(colors))
        # self.res = -1

        # def dfs(node):
        #     # print(node)
        #     color = colors[node]
        #     visisted.add(node)
        #     color_counts.remove((color_d[color], color))
        #     color_d[color] += 1
        #     color_counts.add((color_d[color], color))
        #     self.res = max(self.res, color_counts[-1][0])

        #     for other in edge_d[node]:
        #         if other not in visisted:
        #             dfs(other)

        #     visisted.remove(node)
        #     color_counts.remove((color_d[color], color))
        #     color_d[color] -= 1
        #     color_counts.add((color_d[color], color))

        # for i in range(n):
        #     if indgree_d[i] == 0:
        #         dfs(i)

        # return self.res
        # end

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))  # 26
print(f(colors="abaca", edges=[[0,1],[0,2],[2,3],[3,4]]))  # 3
print(f(colors="a", edges=[[0,0]]))  # -1
