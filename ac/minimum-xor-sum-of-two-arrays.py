
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
    def calculate_cuts(self, nums1: list[int], nums2: list[int]) -> int:
        # begin
        # import itertools as it
        import math
        from functools import lru_cache
        
        def mask_to_digit(mask: int):
            while mask:
                i = mask & -mask
                yield int(math.log2(i))
                mask = mask ^ i
            yield from ()

        @lru_cache(maxsize=None)
        def dp(mask: int, n: int) -> int:
            """
            mask belong nums2 and there are n 1 digit.
            find min xor sum of nums1[:n] and nums2[mask]
            """
            if n == 0:
                return 0
            res = 10**9
            for i in mask_to_digit(mask):
                _ = (nums1[n - 1] ^ nums2[i]) + dp(mask ^ (1 << i), n - 1)
                res = min(res, _)
            return res

        n = len(nums1)
        return dp((1 << n) - 1, n)
        # end

f = SectionCut().calculate_cuts
print(f([1,2], [2,3]))
print(f([1,0,3], [5,3,4]))
