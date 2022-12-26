# leetcode-clt
leetcode command line tool


## minimum-incompatibility
我的答案是5000ms，这个解是100ms但是看不懂。以后再研究一下。。
https://leetcode.com/problems/minimum-incompatibility/discuss/961672/Python-DFS-backtracking-pruning-(~100-ms)


## minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits.py
这个题太难了。做了好几天都没做出来。最后在hint下实现了

## smallest-rotation-with-highest-score
这个题用O(nlogn)AC了，但是有O(n)的解没看懂: https://leetcode.com/problems/smallest-rotation-with-highest-score/discuss/1982967/Python-with-explanation-in-comments


## zuma-game
TLE，最好的成绩pass (n-2)/n。感觉没有优化的空间了。心累

## maximum-segment-sum-after-removals
为什么runtime_percentile只有5%?


## minimum-total-distance-traveled
这些解太难理解了：https://leetcode.com/problems/minimum-total-distance-traveled/solutions/2786768/python-dp-o-n-m-log-n/
https://leetcode.com/problems/minimum-total-distance-traveled/solutions/2783245/Python3-O(MN)-DP/
迷茫


## minimum-total-cost-to-make-arrays-unequal
有个更风骚的解法，代码更短，但不好理解
```
class Solution:
    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:
        if max((Counter(nums1) + Counter(nums2)).values()) > len(nums1): return -1 
        ans = 0
        diff = []
        cand = vote = 0 
        for i, (x, y) in enumerate(zip(nums1, nums2)): 
            if x == y: 
                ans += i 
                if x == cand or not vote: 
                    cand = x 
                    vote += 1
                else: vote -= 1
            else: diff.append(i)
        for i in diff: 
            if cand not in (nums1[i], nums2[i]) and vote: 
                ans += i 
                vote -= 1
        return ans
```