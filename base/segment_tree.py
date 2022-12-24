from dataclasses import dataclass
from functools import cached_property
from typing import Optional


@dataclass
class STNode(object):
    lo: int
    hi: int
    metric: int = 0
    left_child: Optional["STNode"] = None
    right_child: Optional["STNode"] = None

    @cached_property
    def mid(self) -> int:
        return (self.lo + self.hi) >> 1

    def build(self):
        if self.lo == self.hi:
            return

        if not self.left_child:
            self.left_child = STNode(lo=self.lo, hi=self.mid, metric=self.metric)
            self.left_child.build()
        if not self.right_child:
            self.right_child = STNode(lo=self.mid + 1, hi=self.hi, metric=self.metric)
            self.right_child.build()

    def update(self, k, v):
        self.metric = max(self.metric, v)
        if self.lo == self.hi == k:
            return
        if k > self.mid:
            self.right_child.update(k, v)
        else:
            self.left_child.update(k, v)

    def query(self, lo, hi) -> int:
        if lo == self.lo and hi == self.hi:
            return self.metric
        if lo > self.mid:
            return self.right_child.query(lo, hi)
        if hi <= self.mid:
            return self.left_child.query(lo, hi)
        return max(
            self.left_child.query(lo, self.mid),
            self.right_child.query(self.mid + 1, hi),
        )
