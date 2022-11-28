
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
    def minInsertions(self, nums: list[int], numsDivide: list[int]) -> int:
        # begin
        def gcd(a, b):
            while a % b:
                a, b = b, a % b
            return b

        cd = numsDivide[0]
        for i in range(1, len(numsDivide)):
            cd = gcd(cd, numsDivide[i])
        
        nums.sort()
        for i, v in enumerate(nums):
            if cd % v == 0:
                return i
        return -1

        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
print(f([2,3,2,4,3], numsDivide = [9,6,9,3,15]))
print(f([4,3,6], numsDivide = [8,2,6,10]))
