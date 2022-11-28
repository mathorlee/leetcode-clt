class SectionCut(object):
    def f(self, rectangles):
        # begin
        from dataclasses import dataclass
        from collections import deque

        def range_overlap(r1, r2):
            arr = sorted([*r1, *r2])
            x0, x1 = arr[1], arr[2]
            if x0 < x1:
                x = (x0 + x1) / 2
                if r1[0] < x < r1[1]:
                    return (x0, x1)
            return None

        @dataclass
        class Recangle:
            x: int
            y: int
            x1: int
            y1: int

            @property
            def W(self):
                return self.x1 - self.x
            
            @property
            def L(self):
                return self.y1 - self.y

            @property
            def area(self):
                return self.W * self.L

            @property
            def x_range(self):
                return (self.x, self.x1)

            @property
            def y_range(self):
                return (self.y, self.y1)

            def clone(self, **kwargs):
                return Recangle(
                    x=kwargs.get("x", self.x),
                    y=kwargs.get("y", self.y),
                    x1=kwargs.get("x1", self.x1),
                    y1=kwargs.get("y1", self.y1),
                )

            def sub(self, other) -> list:
                x_range = range_overlap(self.x_range, other.x_range)
                if x_range:
                    y_range = range_overlap(self.y_range, other.y_range)
                    if y_range:
                        ret = []
                        _ = self.clone(x1=x_range[0])
                        if _.W > 0:
                            ret.append(_)
                        _ = self.clone(x=x_range[1])
                        if _.W > 0:
                            ret.append(_)
                        _ = Recangle(x=x_range[0], x1=x_range[1], y=self.y, y1=y_range[0])
                        if _.L > 0:
                            ret.append(_)
                        _ = Recangle(x=x_range[0], x1=x_range[1], y=y_range[1], y1=self.y1)
                        if _.L > 0:
                            ret.append(_)
                        return ret
                return [self]

        M = 10**9 + 7
        q = deque()
        for _ in rectangles:
            r1 = Recangle(x=_[0], y=_[1], x1=_[2], y1=_[3])
            for i in range(len(q)):
                r2 = q.popleft()
                q.extend(r2.sub(r1))
            q.append(r1)
            print(q)

        res = 0
        for _ in q:
            res = (res + _.area) % M
        return res
        # end

f = SectionCut().f
print(f([[0,0,2,2],[1,0,2,3],[1,0,3,1]]))
