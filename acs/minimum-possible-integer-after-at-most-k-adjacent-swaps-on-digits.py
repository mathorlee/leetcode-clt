
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
    def minInsertions(self, num: str, k: int) -> str:
        # begin
        from sortedcontainers import SortedList

        n = len(num)
        window = SortedList()  # sliding window of size k + 1, store (value, index) of num
        indices = SortedList(range(n))  # remained indices
        res = []

        while k > 0:
            # add to remain window size to k + 1
            while len(window) < k + 1 and len(window) < len(indices):
                _ = indices[len(window)]
                window.add((num[_], _))

            # empty window, break
            if not window:
                break

            # pop minimum value
            index = window.pop(0)[1]
            res.append(index)
            k -= indices.bisect_left(index)
            indices.remove(index)

            # remove to remain window size to k + 1
            for _ in indices[k + 1: len(window)]:
                window.remove((num[_], _))

        s0 = set(res)
        return "".join(num[j] for j in res) + "".join(num[j] for j in range(n) if j not in s0)
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
input = read_input()
print(f(*input))
# print(f("4321", 4))  # 1342
# print(f("100", 1))
# print(f("36789", 1000))
# print(f("294984148179", 11))  # 124498948179
# print(f("412465599017575959104005", 22))  # 011244556979575959104005