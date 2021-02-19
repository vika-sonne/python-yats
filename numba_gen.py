
import array
import math
from numba.pycc import CC

cc = CC('numba_run')
# Uncomment the following line to print out the compilation steps
# cc.verbose = True

# @cc.export('multf', 'f8(f8[:])')
# @cc.export('multi', 'i4(i4[:])')
# @cc.export('multii', 'i8(i8[:])')
# @cc.export('multu', 'u4(u4[:])')
# @cc.export('multuu', 'u8(u8[:])')
@cc.export('multi', 'i4(i4, i4)')
def mult(a, b):
	count = 1_000_000
	buff = [1] * count
	for _ in range(len(buff)):
		buff[_] = a * b
	return buff[0]

@cc.export('power', 'f8(f8)')
def power(a):
	count = 1_000_000
	b = 0
	for _ in range(count):
		b += a ** 2
	return b

@cc.export('sqrt', 'f8(f8)')
def sqrt(a):
	count = 1_000_000
	b = 0.
	for _ in range(count):
		b += math.sqrt(a)
	return b

if __name__ == "__main__":
	cc.compile()
