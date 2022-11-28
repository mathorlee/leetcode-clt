class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right




class SectionCut(object):
    def f(self, nums: list[int], lower: int, upper: int) -> int:
        # begin
        from sortedcontainers import SortedList
        
        pre_sums = SortedList()
        pre_sum = 0
        res = 0
        for _ in nums:
            pre_sum += _
            res = res + pre_sums.bisect_right(pre_sum - lower) - pre_sums.bisect_left(pre_sum - upper) + (lower <= pre_sum <= upper)
            pre_sums.add(pre_sum)
        return res
        # end

print(SectionCut().f([-2,5,-1], -2, 2))
