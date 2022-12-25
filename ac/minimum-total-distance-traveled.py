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

    def calculate_cuts(self, robot: list[int], factory: list[list[int]]) -> int:
        # begin
        import bisect
        from functools import cache

        robot.sort()
        factory.sort(key=lambda _: _[0])

        limits = []
        for _, limit in factory:
            limits.append(limits[-1] + limit if limits else limit)
        robot_pos_presum = [0]
        for _ in robot:
            robot_pos_presum.append(robot_pos_presum[-1] + _)

        def _robots_move_to_pos(lo: int, hi: int, pos: int) -> int:
            return abs(robot_pos_presum[hi] - robot_pos_presum[lo] - (hi - lo) * pos)

        def robots_move_to_pos(lo: int, hi: int, pos: int) -> int:
            index = bisect.bisect_left(robot, pos, lo, hi)
            if index >= hi or index == lo:
                return _robots_move_to_pos(lo, hi, pos)
            return _robots_move_to_pos(lo, index, pos) + _robots_move_to_pos(index, hi, pos)
            # return sum(abs(pos - robot[i]) for i in range(lo, hi))

        @cache
        def dp(n_factory: int, n_robot: int) -> int:
            """factory[:n_factory + 1]修理robot[:n_robot]的最小cost"""
            if n_robot > limits[n_factory]:
                return -1
            if n_robot == 0:
                return 0
            pos, limit = factory[n_factory]
            if n_factory == 0:
                return robots_move_to_pos(0, n_robot, pos)

            res = float("inf")
            for k in range(min(limit, n_robot), -1, -1):
                _ = dp(n_factory - 1, n_robot - k)
                if _ == -1:
                    break
                _ += robots_move_to_pos(n_robot - k, n_robot, pos)
                res = min(res, _)
            return res  # type: ignore

        return dp(len(factory) - 1, len(robot))
        # end

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))  # [1,1,2,2,2,2,2,2,2,1]
print(f(robot=[0,4,6], factory=[[2,2],[6,2]]))  # 4
print(f(robot=[1,-1], factory=[[-2,1],[2,1]]))  # 2