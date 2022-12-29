def kmp_pattern(s):
    ret = [0] * len(s)
    for i in range(1, len(s)):
        j = ret[i - 1]
        while j > 0 and s[i] != s[j]:
            j = ret[j - 1]
        if s[i] == s[j]:
            j += 1
        ret[i] = j
    return ret
