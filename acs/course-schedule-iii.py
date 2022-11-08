class SectionCut(object):
    def calculate_cuts(self, courses: list[list[int]]) -> int:
        # begin
        from sortedcontainers import SortedList

        courses.sort(key=lambda _: _[1])
        arr = SortedList()
        total_cost = 0
        for cost, ddl in courses:
            if total_cost + cost <= ddl:
                arr.add(cost)
                total_cost += cost
            elif arr and arr[-1] > cost:
                total_cost = total_cost - arr[-1] + cost
                arr.pop()
                arr.add(cost)
        return len(arr)
        # end

f = SectionCut().calculate_cuts
print(f([[100,200],[200,1300],[1000,1250],[2000,3200]]))
