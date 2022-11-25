
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
    def minInsertions(self, words: list[str]) -> list[int]:
        # begin
        class Node():
            def __init__(self) -> None:
                self.v = 0
                self.children = {}

        root = Node()
        for word in words:
            node = root
            for c in word:
                if c not in node.children:
                    node.children[c] = Node()
                node = node.children[c]
                node.v += 1

        res = []
        for word in words:
            node = root
            v = 0
            for c in word:
                if c in node.children:
                    node = node.children[c]
                    v += node.v
            res.append(v)
        return res
        # end

def read_input():
    import os
    path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path, "r") as f:
        return [eval(_) for _ in f.read().split("\n")]

f = SectionCut().minInsertions
# input = read_input()
# print(f(*input))
# print(f("4321", 4))  # 1342
# print(f("100", 1))
# print(f("36789", 1000))
print(f(["abc","ab","bc","b"]))
print(f(["abcd"]))