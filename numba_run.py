#!/usr/bin/env python3

import sys
from platform import python_version
import time
import array
import math
import statistics


tests_count = 7
test_name1 = 'array_creation_set_by_index'
test_name2 = 'exponentiation'
test_name3 = 'sqrt'
delimiter = ','

def run_test(test_func, impl_name, test_name):

	def print_result(implementation, test_name):
		print(f'{implementation}{delimiter}{test_name}{delimiter}', end='')
		print(f'{statistics.mean(time_results):1.3}{delimiter}{min(time_results):1.3}{delimiter}{max(time_results):1.3}'
			f'{delimiter}{max(time_results)-min(time_results):1.3}')

	time_results = [] # tests time measurements
	for _ in range(tests_count):
		t = time.perf_counter()
		test_func()
		elapsed_time = time.perf_counter() - t
		time_results.append(elapsed_time)
	print_result(impl_name, test_name)

if sys.implementation.name != 'pypy': # since pypy don't import generated module by numba
	import numba_run

	def numba_multi():
		numba_run.multi(3, 4)

	def numba_power():
		numba_run.power(1.41)

	def numba_sqrt():
		numba_run.sqrt(1.41)

	print(f'implementation{delimiter}name{delimiter}avg{delimiter}min{delimiter}max{delimiter}delta')

	numba_name = f'numba {python_version()}'
	run_test(numba_multi, numba_name, test_name1)
	run_test(numba_power, numba_name, test_name2)
	run_test(numba_sqrt, numba_name, test_name3)

def python_multi():
	count = 1_000_000
	a, b = 3, 4
	c = [1] * count
	for _ in range(count):
		c[_] = a * b

def python_power():
	count = 1_000_000
	a, b = 1.41, 0
	for _ in range(count):
		b += a ** 2

def python_sqrt():
	count = 1_000_000
	a, b = 1.41, 0.
	for _ in range(count):
		b += math.sqrt(a)

impl_name = f'{sys.implementation.name} {python_version()}'
run_test(python_multi, impl_name, test_name1)
run_test(python_power, impl_name, test_name2)
run_test(python_sqrt, impl_name, test_name3)
