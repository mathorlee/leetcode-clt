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

    def calculate_cuts(self, piles: list[list[int]], k: int) -> int:
        # begin
        """
        dp[n][k] = max(dp[n - 1][k], dp[n - 1][k - 1] + piles[i][:1], ...)
        """
        from functools import lru_cache

        counts = []
        # piles -> pre sums
        for coins in piles:
            for i in range(1, len(coins)):
                coins[i] += coins[i - 1]
            if counts:
                counts.append(len(coins) + counts[-1])
            else:
                counts.append(len(coins))

        @lru_cache(None)
        def dp(n, k):
            """piles[:n]拿k个"""
            if counts[n] < k:
                return -1

            if k == 0:  # 拿0个，得分0
                return 0

            coins = piles[n]
            if n == 0:  # 从piles[0]拿k个
                return coins[k - 1]

            res = 0
            for i in range(min(k, len(coins)), -1, -1):  # piles[n]取i个
                _ = dp(n - 1, k - i)
                if _ == -1:
                    break
                if i:
                    _ += coins[i - 1]
                res = max(res, _)
            return res

        return dp(len(piles) - 1, k)
        # end

f = SectionCut().calculate_cuts
# input = read_input()
# print(f(*input))  # [1,1,2,2,2,2,2,2,2,1]
print(f(piles=[[1,100,3],[7,8,9]], k=2))  # 101
print(f(piles=[[100],[100],[100],[100],[100],[100],[1,1,1,1,1,1,700]], k=7))  # 706