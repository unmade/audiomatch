# cython: language_level=3

cimport cython
from libc.stdint cimport uint32_t

cdef extern int __builtin_popcount(unsigned int) nogil


def popcount(uint32_t x):
    return __builtin_popcount(x)
