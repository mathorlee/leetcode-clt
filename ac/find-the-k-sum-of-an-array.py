def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

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


def k_array(s):
    ret = [0] * len(s)
    for i in range(1, len(s)):
        j = ret[i - 1]
        while j > 0 and s[i] != s[j]:
            j = ret[j - 1]
        if s[i] == s[j]:
            j += 1
        ret[i] = j
    return ret


class SectionCut(object):
    def minInsertions(self, nums: list[int], k: int) -> int:
        # begin
        """
        1: delete abs(nums[_]), 0: do not delete abs[nums[_]] from max_value
        FSM(有限状态机) is a full binary tree
        1
            11
                111
                101
            01
                011
                001
        binary tree must satisfy:
            1. child != father + "0"
            2. each node at least one digit is "1"
        """
        from sortedcontainers import SortedList

        max_value = sum(_ for _ in nums if _ > 0)
        nums = sorted(abs(_) for _ in nums)
        sl = SortedList([(max_value, 0)])  # sub first element

        for _ in range(k):
            v, index = sl.pop(-1)
            if index < len(nums):
                sl.add((v - nums[index], index + 1))
                if index > 0:
                    sl.add((v + nums[index - 1] - nums[index], index + 1))
        return v
        # end

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
print(f(nums=[2,4,-2], k=5))  # 2
print(f(nums=[1,-2,3,4,-10,12], k=16))  # 10