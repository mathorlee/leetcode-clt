
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
    def calculate_cuts(self, target: list[int], arr: list[int]) -> int:
        # begin
        from bisect import bisect_left
        
        index_d = {v: i for i, v in enumerate(target)}
        
        # solution 1: TLE
        # res = [0] * len(target)
        # for v in arr:
        #     if v in index_d:
        #         index = index_d[v]
        #         if index > 0:
        #             res[index] = max(res[:index]) + 1
        #         else:
        #             res[index] = 1
        # return len(target) - max(res)

        # solution 2: 
        res = []  # res[i] = min(v if subsequence length = i + 1 and subsequence end with target[v])
        for v in arr:
            if v in index_d:
                index = index_d[v]
                i = bisect_left(res, index)
                if i < len(res):
                    res[i] = min(res[i], index)
                else:
                    res.append(index)
        return len(target) - len(res)
        # end

f = SectionCut().calculate_cuts
# print(f([5,1,3], [9,4,2,3,4]))
print(f([6,4,8,1,3,2], [4,7,6,2,3,8,6,1]))
