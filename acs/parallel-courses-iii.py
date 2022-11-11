
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
    
    def xx(self, n: int, relations: list[list[int]], time: list[int]) -> int:
        # begin
        from collections import defaultdict, deque

        degrees = [0] * n  # in degree
        begin_times = [0] * n

        edge_d = defaultdict(list)
        for a, b in relations:
            a -= 1
            b -= 1
            edge_d[a].append(b)
            degrees[b] += 1

        q = deque()
        for i, degree in enumerate(degrees):
            if degree == 0:
                q.append(i)
        while q:
            i = q.popleft()
            for j in edge_d[i]:
                begin_time = begin_times[i] + time[i]
                begin_times[j] = max(begin_time, begin_times[j])
                degrees[j] -= 1
                if degrees[j] == 0:
                    q.append(j)

        return max(begin_times[i] + time[i] for i in range(n))
        # end

f = SectionCut().xx
print(f(3, [[1,3],[2,3]], [3,2,5]))
print(f(5, [[1,5],[2,5],[3,5],[3,4],[4,5]], [1,2,3,4,5]))
