class SectionCut(object):
    def f(self, nums, target):
        # begin
        ret = []
        arr = sorted(nums)
        n  = len(arr)

        def b_search(value, left, right, arr):
            while left + 1 < right:
                middle = (left + right) // 2
                if arr[middle] == value:
                    return middle
                if arr[middle] > value:
                    right = middle
                elif arr[middle] < value:
                    left = middle
            if arr[left] == value:
                return left
            if arr[right] == value:
                return right
            return -1

        index = -1
        for i in range(n - 1):
            small = arr[i]
            index = b_search(target - small, i + 1, n - 1, arr)
            if index != -1:
                break

        for i in range(n):
            if nums[i] == small or nums[i] == target - small:
                ret.append(i)
                if len(ret) == 2:
                    break

        return sorted(ret)
        # end
print(SectionCut().f([2,7,11,15], 9))