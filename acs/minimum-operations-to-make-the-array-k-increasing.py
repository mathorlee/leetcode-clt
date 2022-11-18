
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
    def calculate_cuts(self, arr: list[int], k: int) -> int:
        # begin
        from bisect import bisect_right

        n = len(arr)
        res = 0
        for i in range(k):
            values = []
            cnt = 0
            for j in range(i, n, k):
                cnt += 1
                v = arr[j]
                index = bisect_right(values, v)
                if index < len(values):
                    values[index] = min(values[index], v)
                else:
                    values.append(v)
            res += cnt - len(values)
        return res
        # end

f = SectionCut().calculate_cuts
# print(f([5,4,3,2,1], 1))
print(f([4,1,5,2,6,2], 2))
