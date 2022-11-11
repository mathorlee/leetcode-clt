
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
    
    def xx(self, s: str) -> int:
        # begin

        n = len(s)
        d = {}  # char last appear position
        arr = [0] * n  # sum(appear(_) for _ in (s[0: i + 1], ..., s[i: i + 1]))
        arr[0] = 1
        d[s[0]] = 0

        for i in range(1, n):
            if s[i] == s[i - 1]:
                arr[i] = arr[i - 1] + 1
            else:
                if s[i] in d:
                    arr[i] = arr[i - 1] + i - d[s[i]]
                else:
                    arr[i] = arr[i - 1] + i + 1
            d[s[i]] = i

        print(arr)
        return sum(arr)
        # end

f = SectionCut().xx
print(f("fluqu"))
# print(f("abb"))
