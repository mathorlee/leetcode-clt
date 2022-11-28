
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

def mask_to_bits(mask: int):
    import math
    while mask:
        i = mask & -mask
        yield int(math.log2(i))
        mask = mask ^ i
    yield from ()


class SectionCut(object):
    def minInsertions(self, nums: list[int], cost: list[int]) -> int:
        # begin
        n = len(nums)
        arr = sorted(zip(nums, cost))  # 按照数字大小排序
        increse_costs = [0] * n  # increse_costs[i]: 所有num修改为arr[i][0]，给num做增加操作的花费
        decrese_costs = [0] * n  # decrese_costs[i]: 所有num修改为arr[i][0]，给num做减少操作的花费

        # DP. bandwidth: cost总带宽
        bandwidth = arr[0][1]
        for i in range(1, n):
            increse_costs[i] = (arr[i][0] - arr[i - 1][0]) * bandwidth + increse_costs[i - 1]
            bandwidth += arr[i][1]

        bandwidth = arr[-1][1]
        for i in range(n - 2, -1, -1):
            decrese_costs[i] += (arr[i + 1][0] - arr[i][0]) * bandwidth + decrese_costs[i + 1]
            bandwidth += arr[i][1]

        # print(arr)
        # print(increse_costs)
        # print(decrese_costs)
        return min(increse_costs[_] + decrese_costs[_] for _ in range(n))
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
print(f(nums = [1,3,5,2], cost = [2,3,1,14]))
print(f([2,2,2,2,2], cost = [4,2,8,1,3]))
