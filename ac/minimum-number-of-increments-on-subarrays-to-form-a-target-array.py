
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


class SectionCut(object):
    def calculate_cuts(self, target: list[int]) -> int:
        # begin
        # import itertools as it
        # import math
        # from functools import lru_cache
        stack = []
        res = 0
        for x in target:
            if stack and x < stack[-1]:
                res += stack.pop() - x
            while stack and x <= stack[-1]:
                stack.pop()
            stack.append(x)
        # print(stack, res)
        res += stack[-1]
        return res
        # end

f = SectionCut().calculate_cuts
# print(f([1,2,3,2,1]))
# print(f([3,1,1,2]))
# print(f([3,1,5,4,2]))
print(f([3,4,2,5,6]))