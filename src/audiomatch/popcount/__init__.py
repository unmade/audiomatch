try:
    from audiomatch.popcount._popcount import popcount
except ImportError:
    # Source:
    #     http://www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
    #
    # This popcount version works slightly faster than 'bin(x).count("1")'

    def _popcount_table(size):
        table = [0] * 2 ** size
        for i in range(len(table)):
            table[i] = (i & 1) + table[i >> 1]
        return table

    _POPCOUNT_TABLE16 = _popcount_table(16)

    def popcount(x):
        return _POPCOUNT_TABLE16[x & 0xFFFF] + _POPCOUNT_TABLE16[(x >> 16) & 0xFFFF]
