class SectionCut(object):
    def calculate_cuts(self, nums: list[int], indexDiff: int, valueDiff: int) -> bool:
        # begin
        from sortedcontainers import SortedList
        arr = SortedList()
        for i, num in enumerate(nums):
            if i > indexDiff:
                arr.remove(nums[i - indexDiff - 1])
            a, b = arr.bisect_left(num - valueDiff), arr.bisect_right(num + valueDiff)
            if a < b:
                return True
            arr.add(num)
        return False
        # end

f = SectionCut().calculate_cuts
print(f([1,2,3,1], 3, 0))
print(f([1,5,9,1,5,9], 2, 3))
