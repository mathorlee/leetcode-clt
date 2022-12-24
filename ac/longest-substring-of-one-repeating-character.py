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

    def calculate_cuts(self, s: str, queryCharacters: str, queryIndices: list[int]) -> list[int]:
        # begin
        from sortedcontainers import SortedList

        ranges = SortedList()  # 计算ranges
        max_lengths = SortedList()  # [(substring length, begin index)]
        def add_range(lo, hi):
            ranges.add((lo, hi))
            max_lengths.add(hi - lo)

        def del_range(lo, hi):
            ranges.remove((lo, hi))
            max_lengths.remove(hi - lo)

        n = len(s)
        pre = 0
        for i in range(1, n):
            if s[i] != s[pre]:
                add_range(pre, i)  # s[pre:i]
                pre = i
        add_range(pre, n)

        ret = []
        s1 = [_ for _ in s]
        loop = 0
        for c, i in zip(queryCharacters, queryIndices):
            loop += 1
            if s1[i] != c:
                index = min(ranges.bisect_left((i, 0)), len(ranges) - 1)
                lo, hi = ranges[index]
                if lo > i:
                    index -= 1
                    lo, hi = ranges[index]
                new_lo, new_hi = i, i + 1
                if hi < n and i == hi - 1 and s1[hi] == c:
                    right_lo, right_hi = ranges[index + 1]
                    del_range(right_lo, right_hi)
                    new_hi = max(new_hi, right_hi)
                if i > 0 and i == lo and s1[i - 1] == c:
                    left_lo, left_hi = ranges[index - 1]
                    del_range(left_lo, left_hi)
                    new_lo = min(new_lo, left_lo)
                del_range(lo, hi)
                add_range(new_lo, new_hi)
                if new_lo > lo:
                    add_range(lo, new_lo)
                if new_hi < hi:
                    add_range(new_hi, hi)
                s1[i] = c
            ret.append(max_lengths[-1])
            # print("".join(s1), ret[-1], list(ranges))
        return ret
        # end

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))  # [1,1,2,2,2,2,2,2,2,1]
print(f(s="babacc", queryCharacters="bcb", queryIndices=[1,3,3]))  # [3,3,4]
print(f(s="abyzz", queryCharacters="aa", queryIndices=[2,1]))  # [2,3]
