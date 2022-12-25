from typing import Dict, List


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

    def calculate_cuts(self, nums1: List[int], nums2: List[int]) -> int:
        # begin
        """
        参考了：https://leetcode.com/problems/minimum-total-cost-to-make-arrays-unequal/solutions/2898175/pigeonhole-with-o-n-algorithm/
        狗日的这个题真的难，思路清奇，角度刁钻！没有这个参考绝对搞不出来。下面这段对equals的奇偶判断，惊为天人！
        ```
        Step3. No dominate number can be guaranteed now.
        If |S| is even, we can always find a way to swap the numbers in pairs so that the result is valid.
        What about |S| is odd?
        a) |S| is odd and 0 belongs to S. We can always find {0, i, j} within S. swap(0, i) and swap (0, j). In other words, 0 used twice.
        b) |S| is odd and 0 doesn't belongs to S. Simply insert 0 to S.
        """
        from collections import Counter

        n = len(nums1)
        equals = []
        nonequals = []
        for i in range(n):
            if nums1[i] != nums2[i]:
                nonequals.append(i)
            else:
                equals.append(i)

        if not equals:
            return 0

        d = Counter(nums1[_] for _ in equals)
        max_repeat_count = max(d.values())
        max_repeat_key = -1  # equal里出现最多的数
        for k, v in d.items():
            if v == max_repeat_count:
                max_repeat_key = k
                break

        missing = max_repeat_count * 2 - len(equals)
        if missing > 0:  #[1, 2, 2]。2的数量过半，需要加missing个nonequals进来
            if len(nonequals) < missing:
                return -1
            for i in nonequals:
                if nums1[i] != max_repeat_key and nums2[i] != max_repeat_key:
                    equals.append(i)
                    missing -= 1
                    if missing == 0:
                        break
        if missing > 0:
            return -1

        return sum(equals)
        # end

f = SectionCut().calculate_cuts
input = read_input()
print(f(*input))  # 210
# print(f(nums1=[1,2,3,4,5], nums2=[1,2,3,4,5]))  # 10
# print(f(nums1=[2,2,2,1,3], nums2=[1,2,2,3,3]))  # 10
# print(f(nums1=[1,2,2], nums2=[1,2,2]))  # -1