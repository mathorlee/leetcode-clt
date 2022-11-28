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
        
    
    def xx(self, n: int) -> int:
        # begin
        from collections import defaultdict
        import itertools

        all_states = [_ for _ in itertools.product(range(3), repeat=3) if _[0] != _[1] and _[1] != _[2]]
        m = len(all_states)
        if n == 1:
            return m

        # init state transfer, store into edge_d
        edge_d = defaultdict(list)
        for i, j in itertools.combinations(range(m), 2):
            if all(all_states[i][k] != all_states[j][k] for k in range(3)):
                edge_d[i].append(j)
                edge_d[j].append(i)
        
        M = 10**9 + 7
        arr = [1] * m
        for _ in range(n - 1):
            new_arr = [0] * m
            for i in range(m):
                for j in edge_d[i]:
                    new_arr[j] = (new_arr[j] + arr[i]) % M
            arr = new_arr
        return sum(arr) % M
        # end

# f = SectionCut().calculate_cuts
# print(f([2,3,1,4,0]))
# print(f([1,3,0,2,4]))
f = SectionCut().xx
print(f(5000))
