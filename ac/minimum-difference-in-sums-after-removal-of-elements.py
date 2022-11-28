
def binary_of_int(i: int, width: int) -> str:
    if i >= 0:
        return f"%0{width}d" % int(bin(i)[2:])
    
    # if i < 0, binary(i) = 反码(binary(-i - 1))
    s = ""
    for _ in binary_of_int(-i - 1, width):
        if _ == "1":
            s += "0"
        else:
            s += "1"
    return s

def mask_to_digit(mask: int):
    import math
    while mask:
        i = mask & -mask
        yield int(math.log2(i))
        mask = mask ^ i
    yield from ()


class SectionCut(object):
    def calculate_cuts(self, nums: list[int]) -> int:
        # begin
        # 0,1,2,3,4,5
        from sortedcontainers import SortedList

        n = len(nums) // 3
        arr = SortedList(nums[:n])
        lft_sums = [sum(arr)]
        for i in range(n, n * 2):
            v = nums[i]
            arr.add(v)
            lft_sums.append(lft_sums[-1] + v - arr.pop())
        
        arr = SortedList(nums[-n:])
        rgt_sums = [sum(arr)]
        for i in range(2 * n - 1, n - 1, -1):
            v = nums[i]
            arr.add(v)
            rgt_sums.append(rgt_sums[-1] + v - arr.pop(0))

        return min(lft_sums[i] - rgt_sums[n - i] for i in range(n + 1))
        # end

f = SectionCut().calculate_cuts
print(f([3,1,2]))
print(f([7,9,5,8,1,3]))
print(f([16,46,43,41,42,14,36,49,50,28,38,25,17,5,18,11,14,21,23,39,23]))
print(f([1,1,1,100,200,600,400,1,1]))