class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right




class SectionCut(object):
    def f(self, formula: str) -> str:
        # begin
        from sortedcontainers import SortedDict

        parentheses = []
        chars = []
        i = 0
        p_range = None
        # a(bc)d, p_range=(1, 3)
        while i < len(formula):
            c = formula[i]
            if c == "(":
                parentheses.append(len(chars))
            elif c == ")":
                p_range = (parentheses.pop(), len(chars))
            elif c.isdigit():
                j = i
                while i + 1 < len(formula) and formula[i + 1].isdigit():
                    i += 1
                x = int(formula[j:i + 1])
                if p_range:
                    for _ in range(*p_range):
                        chars[_][1] *= x
                    p_range = None
                elif chars[-1]:
                    chars[-1][1] *= x
                else:
                    raise Exception(f"no char before nums {x}, illegal")
            elif c.isupper():
                chars.append([c, 1])
                p_range = None
            elif c.islower():
                chars[-1][0] += c
                p_range = None
            i += 1
        
        d = SortedDict()
        for c, cnt in chars:
            d[c] = d.get(c, 0) + cnt
        return "".join(f"{k}{v}" if v > 1 else k for k, v in d.items())
        # end

f = SectionCut().f
print(f("H2O"))
print(f("Mg(OH)X2"))
print(f("K4(ON(SO3)2)2"))
