import math


def radix_sort(a: list[int], radix=10):
    """a为整数列表， radix为基数"""
    K = int(math.ceil(math.log(max(a), radix))) # 用K位数可表示任意整数
    for i in range(K):
        bucket = [[] for i in range(radix)]
        for x in a:
            bucket[x // (radix**i) % radix].append(x)
        a.clear()
        for _ in bucket:
            a.extend(_)
    return a
