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
        import itertools
        from collections import Counter, defaultdict

        def get_primes(N):
            N = N + 1
            is_prime = [True] * N
            for i in range(2, N):
                if is_prime[i]:
                    j = i * 2
                    while j < N:
                        is_prime[j] = False
                        j += i
            return [_ for _ in range(2, N) if is_prime[_]]

        primes, target_node = [], []  # k质数分解
        for _ in get_primes(k):
            i = 0
            while k % _ == 0:
                k //= _
                i += 1
            if i:
                primes.append(_)
                target_node.append(i)
        target_node = tuple(target_node)
        # print(f"primes and counts：{primes} {target_node}")

        def get_prime_counts(k: int, primes: list[int]):
            for _ in primes:
                i = 0
                while k % _ == 0:
                    k //= _
                    i += 1
                yield i
        
        def floor_node(sources):
            return tuple(min(a, b) for a, b in zip(sources, target_node))

        def add_nodes(a, b):
            return tuple(min(a + b, c) for a, b, c in zip(a, b, target_node))

        # AC
        res = 0
        d = defaultdict(int)  # d[tuple] = int
        counter = Counter(floor_node(get_prime_counts(_, primes)) for _ in nums)
        for cur, count in counter.items():
            if d:
                for pre, x in d.items():
                    if add_nodes(cur, pre) == target_node:
                        res += x * count
            d[cur] += count
            if count > 1 and add_nodes(cur, cur) == target_node:
                res += count * (count - 1) // 2
        return res

        # TLE, but better
        # res = 0
        # d = defaultdict(int)  # d[tuple] = int
        # for i, _ in enumerate(nums):
        #     cur = floor_node(get_prime_counts(_, primes))
        #     if i:
        #         if cur == target_node:
        #             res += i
        #         else:
        #             for pre, x in d.items():
        #                 if add_nodes(cur, pre) == target_node:
        #                     res += x
        #     d[cur] += 1
        # return res

        # TLE pass 92/115
        # n = len(nums)
        # m = len(primes)
        # res = 0
        # for i, j in itertools.combinations(range(n), 2):
        #     res += all(arr[i][_] + arr[j][_] >= counts[_] for _ in range(m))
        # return res
        # end

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))  # 1699097284
# print(f(vals=[1,3,2,1,3], edges=[[0,1],[0,2],[2,3],[2,4]]))  # 6
# print(f(vals=[1,1,2,2,3], edges=[[0,1],[1,2],[2,3],[2,4]]))  # 7
# print(f(vals=[1], edges=[]))  # 1
# print(f([2,4,1,2,2,5,3,4,4], [[0,1],[2,1],[0,3],[4,1],[4,5],[3,6],[7,5],[2,8]]))  # 11
# # print(f([2,5,5,1,5,2,3,5,1,5], [[0,1],[2,1],[3,2],[3,4],[3,5],[5,6],[1,7],[8,4],[9,7]]))  # 20
print(f(nums=[1,2,3,4,5], k=2))  # 7
print(f(nums=[1,2,3,4], k=5))  # 0
