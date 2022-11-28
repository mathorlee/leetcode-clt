class SectionCut(object):
    def calculate_cuts(self, s: str, k: int) -> int:
        # begin
        if k > 1:
            return "".join(sorted(s))
        
        return min(s[i:] + s[:i] for i in range(len(s)))

        # from sortedcontainers import SortedList

        # # 132174145
        # def heap_sort(s: str):
        #     ret = []
        #     sl = SortedList()
        #     for _ in s:
        #         sl.add(_)
        #         if len(sl) == k:
        #             ret.append(sl.pop(0))
        #     ret.extend(sl)
        #     return "".join(ret)
        
        # # print(s)
        # res = s
        # # input_s = s
        # while True:
        #     new_s = heap_sort(s)
        #     print(new_s)
        #     res = min(res, new_s)
        #     if new_s == s:
        #         break
        #     s = new_s
        # # if k > 1:
        # #     assert "".join(sorted(input_s)) == s
        # return res
        # end

f = SectionCut().calculate_cuts
# f("132174145", 4)
# f("451321741", 2)
# f("451321741", 2)
print(f("UserssongsongDocumentsprogramdrawingassembledvenvbinpython", 1))
# print(f("eyJ0YWciOiAidjAuNC4xMzUiLCAiZmxvb3JfbnVtYmVyIjogW10sICJmbG9vcl9udW1iZXJfbGlzdCI6IFtdLCAib3V0cHV0X2RyYXdpbmdfbmFtZSI6ICLmpbzmoq/pl7Tor6blm74iLCAib3V0cHV0X2RyYXdpbmdfdHlwZSI6ICLmpbzmoq/pl7Tor6blm74iLCAiZHJhd2luZ19jaGVja19hbnN3ZXJfZCI6IHsi56Kw5aS05qyh5pWwIjogeyJhbnN3ZXIiOiAwLCAiZGVmYXVsdF92YWxpZGF0b3IiOiAiZXEifSwgIueWj+aVo+WNiuW+hOeisOaSniI6IHsiYW5zd2VyIjogMCwgImRlZmF1bHRfdmFsaWRhdG9yIjogImVxIn19LCAiYnVpbGRpbmdfbW9kZWxfcGtsX2ZpbGVfaWQiOiAiZDk4YjYwNmM1MzRkNGE3ZWFjZTM0ZDhiZTlhN2NiMGEifQ", 2))