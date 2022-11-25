
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
    def minInsertions(self, nums: list[int], edges: list[list[int]]) -> int:
        # begin
        from collections import defaultdict

        edge_d = defaultdict(set)
        for a, b in edges:
            edge_d[a].add(b)
            edge_d[b].add(a)

        # init sums
        n = len(nums)
        sums = [0] * n
        def dfs(node) -> int:
            res = nums[node]
            while edge_d[node]:
                other = edge_d[node].pop()
                edge_d[other].remove(node)
                res += dfs(other)
            sums[node] = res
            return res

        dfs(0)

        total = sum(nums)
        for value in range(max(nums), total // 2 + 1):
            if total % value == 0:
                group_count = total // value
                if sum(_ % value == 0 for _ in sums) >= group_count:
                    return group_count - 1
        return 0
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
print(f([1,2,1,1,1], [[0,1],[1,3],[3,4],[4,2]]))