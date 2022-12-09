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

    def calculate_cuts(self, s: str, k: int, minLength: int) -> int:
        # begin
        # from functools import lru_cache
        # import bisect

        # primes = "2357"
        # is_prime = [_ in primes for _ in s]
        # if not is_prime[0] or is_prime[-1]:
        #     return 0
        
        # split_point = []
        # for i in range(1, len(s)):
        #     if is_prime[i] and not is_prime[i - 1]:
        #         split_point.append(i)

        # # TLE 68/73
        # @lru_cache(None)
        # def f(lo, k):
        #     n = len(s) - lo
        #     if n < k * minLength or not is_prime[lo]:
        #         return 0

        #     if k == 1:
        #         return 1

        #     res = 0
        #     max_length = n - (k - 1) * minLength
        #     a = bisect.bisect_left(split_point, lo + minLength)
        #     b = bisect.bisect_left(split_point, lo + max_length)
        #     for _ in range(a, min(b + 1, len(split_point))):
        #         res += f(split_point[_], k - 1)
        #     # for l in range(minLength, max_length + 1):
        #     #     if not is_prime[lo + l - 1]:
        #     #         res += f(lo + l, k - 1)
        #     return res
        # return f(0, k) % (10**9 + 7)

        M = 10**9 + 7
        minLength = max(minLength, 2)
        primes = set("2357")
        is_prime = lambda _: _ in primes

        if not is_prime(s[0]) or is_prime(s[-1]) or k * minLength > len(s):
            return 0

        n = len(s)
        cut_pos = set(i for i in range(n) if not is_prime(s[i]) and (i == n - 1 or is_prime(s[i + 1])))
        is_cut_pos = lambda i: i in cut_pos

        # dp
        dp = [[0] * k for _ in range(n)]
        for i in range(minLength - 1, n):
            dp[i][0] = dp[i - 1][0]  # pre sum
            if is_cut_pos(i):
                dp[i][0] += 1

        for j in range(1, k):
            for i in range(1, n):
                dp[i][j] = dp[i - 1][j]  # pre sum
                if i >= minLength and is_cut_pos(i):
                    dp[i][j] += dp[i - minLength][j - 1]

        # for i, _ in enumerate(dp):
        #     print(_)
        #     if is_cut_pos(i):
        #         print()
        return (dp[n - 1][k - 1] - dp[n - 2][k - 1]) % M
        # end

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))  # 323926698
# print(f(vals=[1,3,2,1,3], edges=[[0,1],[0,2],[2,3],[2,4]]))  # 6
# print(f(vals=[1,1,2,2,3], edges=[[0,1],[1,2],[2,3],[2,4]]))  # 7
# print(f(vals=[1], edges=[]))  # 1
# print(f([2,4,1,2,2,5,3,4,4], [[0,1],[2,1],[0,3],[4,1],[4,5],[3,6],[7,5],[2,8]]))  # 11
# # print(f([2,5,5,1,5,2,3,5,1,5], [[0,1],[2,1],[3,2],[3,4],[3,5],[5,6],[1,7],[8,4],[9,7]]))  # 20
print(f(s="23542185131", k=3, minLength=2))  # 3
print(f(s="23542185131", k=3, minLength=3))  # 1
print(f(s="3312958", k=3, minLength=1))  # 1  "331 | 29 | 58"
