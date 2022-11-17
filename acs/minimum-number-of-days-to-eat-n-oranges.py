
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
    def calculate_cuts(self, n: int) -> int:
        # begin
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(n) -> int:
            if n == 0:
                return 0
            if n % 6 == 0:
                return 1 + min(dp(n // 3), dp(n // 2))
            if n % 3 == 0:
                return min(1 + dp(n // 3), 2 + dp(n // 2))
            if n % 2 == 0:
                return 1 + min(dp(n // 2), dp(n - 1))
            return 1 + dp(n - 1)

        return dp(n)
        # end

f = SectionCut().calculate_cuts
# print(f([5,1,3], [9,4,2,3,4]))
# print(f(10))
# print(f(6))
# print(f(19786))
print(f(84806671))
