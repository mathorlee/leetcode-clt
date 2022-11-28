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
        
    
    def xx(self, n: int, meetings: list[list[int]]) -> int:
        # begin
        from sortedcontainers import SortedList

        meetings.sort()  # 排序
        # print(meetings)
        serve_cnts = [0] * n

        end_times = [0] * n
        for start_time, end_time in meetings:
            # 找在start_time时空闲的编号最小的会议室，如果找不到，找上一个会议结束最早的会议室
            index = -1
            for i in range(n):
                if end_times[i] <= start_time:
                    index = i
                    break
            if index == -1:
                index = end_times.index(min(end_times))  # 上一个会议最早结束的会议室

            serve_cnts[index]+= 1
            end_times[index] = max(start_time, end_times[index]) + end_time - start_time

        # print(serve_cnts)
        x = max(serve_cnts)
        for i, _ in enumerate(serve_cnts):
            if _ == x:
                return i
        # end

# f = SectionCut().calculate_cuts
# print(f([2,3,1,4,0]))
# print(f([1,3,0,2,4]))
f = SectionCut().xx
print(f(2, [[0,10],[1,5],[2,7],[3,4]]))
print(f(3, [[1,20],[2,10],[3,5],[4,9],[6,8]]))
print(f(4, [[18,19],[3,12],[17,19],[2,13],[7,10]]))

# free_times: 8, 5, 4, 10
# start_time: 6, find 4
# start_time: 1, find3