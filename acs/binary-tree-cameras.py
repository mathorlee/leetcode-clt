class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right




class SectionCut(object):
    def f(self, root: TreeNode):
        # begin
        """
        FSM: T/F, T, F
            T/F -> F
            T/F -> T
            if leaf, T/F -> T only
            T -> F
            F -> T/F
        """
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(node: TreeNode, status: str) -> int:
            children = [_ for _ in (node.left, node.right) if _ is not None]
            if status == "T/F":
                if children:
                    # F
                    if len(children) == 1:
                        x = dfs(children[0], "T")
                    else:
                        x = min(
                            dfs(children[0], "T") + dfs(children[1], "T/F"),
                            dfs(children[1], "T") + dfs(children[0], "T/F"),
                        )
                    # T
                    y = 1 + sum(min(dfs(_, "F"), dfs(_, "T")) for _ in children)
                    return min(x, y)
                else:
                    return 1
            elif status == "T":
                return 1 + sum(min(dfs(_, "F"), dfs(_, "T")) for _ in children)
            else:  # F
                return sum(dfs(_, "T/F") for _ in children)

        return dfs(root, "T/F")
        # end

print(SectionCut().f([2,7,11,15], 9))
