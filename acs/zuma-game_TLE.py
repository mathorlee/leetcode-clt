
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
    def minInsertions(self, board: str, hand: str) -> int:
        # begin
        """
        board长度是16，hand长度是5。bfs，找最优解
        """
        from collections import Counter, deque
        from sortedcontainers import SortedList

        hand = "".join(sorted(hand))

        def insert_char_to_str(s: str, c: str, position: int) -> str:
            s = s[:position] + c + s[position:]
            while s:
                i, j = position, position
                while i > 0 and s[i - 1] == s[position]:
                    i -= 1
                while j + 1 < len(s) and s[j + 1] == s[position]:
                    j += 1
                if j - i + 1 >= 3:
                    s = s[:i] + s[j + 1:]
                    if not s:
                        return ""
                    position = max(i - 1, 0)
                else:
                    return s

        M = len(hand)
        visisted = set((board, ))
        q = deque(((board, hand),))

        # bfs
        while q:
            node = q.popleft()
            board, hand = node
            for i, c in enumerate(hand):
                if i > 0 and c == hand[i - 1]:  # optimization 2
                    continue
                new_hand = hand[:i] + hand[i + 1:]
                for j in range(len(board) + 1):
                    # if board[j] == board[j - 1] or c == board[j]:  # optimization 3
                    if len(board) > j > 0 and c == board[j]:
                        continue
                    new_board = insert_char_to_str(board, c, j)
                    if new_board == "":
                        return M - len(new_hand)
                    if new_hand and new_board not in visisted:
                        q.append((new_board, new_hand))
                        visisted.add(new_board)
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
print(f("WRRBBW", "RB"))
print(f("WWRRBBWW", "WRBRW"))
print(f("G", "GGGGG"))
print(f("RRGGBBYYWWRRGGBB", "RGBYW"))
print(f("RRWWRRBBRR", "WB"))  # 2
print(f("RRYGGYYRRYYGGYRR", "GGBBB"))
print(f("YYRGWRBYGGBGBGWY", "BWGRY"))