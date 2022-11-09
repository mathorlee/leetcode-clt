class SectionCut(object):
    def calculate_cuts(self, board: list[list[int]]) -> int:
        # begin
        """
        bfs
        """
        from collections import deque

        def swap(s: str, i0, i1) -> str:
            arr = [_ for _ in s]
            arr[i0], arr[i1] = arr[i1], arr[i0]
            return "".join(arr)

        move_dirs = [
            [1, 3],
            [0, 2, 4],
            [1, 5],
            [0, 4],
            [3, 1, 5],
            [4, 2],
        ]
        q = deque()
        visited = set()
        arr = board[0] + board[1]
        s = "".join(str(_) for _ in arr)
        q.append((s, arr.index(0), 0))
        visited.add(s)
        while q:
            s, i, step_cnt = q.popleft()
            if s == "123450":
                return step_cnt
            for i1 in move_dirs[i]:
                s1 = swap(s, i, i1)
                if s1 not in visited:
                    q.append((s1, i1, step_cnt + 1))
                    visited.add(s1)
        return -1
        # end

f = SectionCut().calculate_cuts
print(f([[1,2,3],[4,0,5]]))
print(f([[1,2,3],[5,4,0]]))
print(f([[4,1,2],[5,0,3]]))
