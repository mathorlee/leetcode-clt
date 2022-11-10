class SectionCut(object):
    def calculate_cuts(self, nums) -> int:
        
        from sortedcontainers import SortedList

        n = len(nums)
        nums = [v - i for i, v in enumerate(nums)]
        lft_arr = SortedList()
        rgt_arr = SortedList(nums)

        score = 0
        index = 0
        for k in range(n):
            _ = rgt_arr.bisect_right(-k) + lft_arr.bisect_right(n - k)
            if _ > score:
                index = k
                score = _
            rgt_arr.remove(nums[k])
            lft_arr.add(nums[k])
        return index
        
    
    def xx(self, grid: list[list[int]]) -> int:
        # begin
        import itertools
        from collections import defaultdict

        m, n = len(grid), len(grid[0])

        def next_cols(col):
            if col > 0:
                yield col - 1
            if col + 1 < n:
                yield col + 1
            yield col

        score_d = {(0, n - 1): grid[0][0] if n == 1 else grid[0][0] + grid[0][-1]}
        for i in range(1, m):
            new_score_d = defaultdict(int)
            for (c0, c1), score in score_d.items():
                for c2, c3 in itertools.product(next_cols(c0), next_cols(c1)):
                    _ = grid[i][c2] if c2 == c3 else grid[i][c2] + grid[i][c3]
                    new_score_d[c2, c3] = max(new_score_d[c2, c3], score + _)
            score_d = new_score_d
        return max(score_d.values())
        # end

# f = SectionCut().calculate_cuts
# print(f([2,3,1,4,0]))
# print(f([1,3,0,2,4]))
f = SectionCut().xx
print(f([[3,1,1],[2,5,1],[1,5,5],[2,1,1]]))
print(f([[1,0,0,0,0,0,1],[2,0,0,0,0,3,0],[2,0,9,0,0,0,0],[0,3,0,5,4,0,0],[1,0,2,3,0,0,6]]))