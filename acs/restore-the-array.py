class SectionCut(object):
    def calculate_cuts(self, s: str, k: int) -> int:
        # begin
        from functools import lru_cache

        M = 10**9 + 7

        @lru_cache(maxsize=None)
        def dfs(index):
            if index == len(s):
                return 1
            res = 0
            for i in range(index, len(s)):
                if 1 <= int(s[index: i + 1]) <= k:
                    res = (res + dfs(i + 1)) % M
                else:
                    break
            return res
        return dfs(0)
        # end

f = SectionCut().calculate_cuts
print(f("1317", 2000))
print(f("1000", 10))
print(f("1000", 10000))