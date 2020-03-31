"""
Source:
    http://www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
"""


def popcount_table16():
    table = [0] * 2 ** 16
    for i in range(len(table)):
        table[i] = (i & 1) + table[i >> 1]
    return table


POPCOUNT_TABLE16 = popcount_table16()


def popcount(x):
    return POPCOUNT_TABLE16[x & 0xFFFF] + POPCOUNT_TABLE16[(x >> 16) & 0xFFFF]
