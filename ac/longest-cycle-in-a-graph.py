
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
    def minInsertions(self, edges: list[int]) -> int:
        # begin
        from collections import defaultdict, deque

        # init indegree and edge dict
        n = len(edges)
        degree = [0] * n
        edge_d = defaultdict(set)
        for i, x in enumerate(edges):
            edge_d[i].add(x)
            degree[x] += 1

        # bfs, delete node of 0 indegree till there are no 0 indegree node
        q = deque(i for i in range(n) if degree[i] == 0)
        while q:
            i = q.popleft()
            for _ in edge_d[i]:
                degree[_] -= 1
                if degree[_] == 0:
                    q.append(_)
            del edge_d[i]

        # remain connect graph must be circles
        res = -1
        visited = set()
        for i in range(n):
            if degree[i] > 0:
                visited.add(i)
                j = i
                cnt = 1
                while edge_d[j]:
                    j = edge_d[j].pop()
                    if j == i:
                        res = max(res, cnt)  # max circle
                        break
                    visited.add(j)
                    cnt += 1
        return res
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
# print(f("4321", 4))  # 1342
# print(f("100", 1))
# print(f("36789", 1000))
# print(f([6,2,2,2,6], edges=[[0,1],[1,2],[1,3],[3,4]]))
# print(f([2], edges=[]))
print(f([3,3,4,2,3]))
print(f([2,-1,3,1]))