#!/usr/bin/env python3

import sys
from platform import python_version
import time
import statistics
import types
import argparse
import array
from typing import List


class test:
	def setup(self):
		pass
	def run(self):
		pass

def test_class(cls):
	cls._is_test = True
	return cls

# --- TESTS ---

# Containers

class l_index_get(test):
	def setup(self):
		self.cycles = 1_000_000
	def run(self):
		buff, buff2 = self.buff, 0
		for _ in range(self.cycles):
			buff2 = buff[_]

class l_index_set(test):
	def setup(self):
		self.cycles = 1_000_000
	def run(self):
		buff = self.buff
		for _ in range(self.cycles):
			buff[_] = 0

@test_class
class list_index_get(l_index_get):
	'buff = list[_]'
	def setup(self):
		super().setup()
		self.buff = [1] * self.cycles

@test_class
class list_index_set(l_index_set):
	'list[_] = 0'
	def setup(self):
		super().setup()
		self.buff = [1] * self.cycles

@test_class
class array_index_get(l_index_get):
	'buff = array[_]'
	def setup(self):
		super().setup()
		self.buff = array.array('I', [1] * self.cycles)

@test_class
class array_index_set(l_index_set):
	'array[_] = 0'
	def setup(self):
		super().setup()
		self.buff = array.array('I', [1] * self.cycles)

@test_class
class memoryview_index_get(l_index_get):
	'buff = memoryview[_]'
	def setup(self):
		super().setup()
		self.buff = memoryview(array.array('I', [1] * self.cycles))

@test_class
class memoryview_index_set(l_index_set):
	'memoryview[_] = 0'
	def setup(self):
		super().setup()
		self.buff = memoryview(array.array('I', [1] * self.cycles))

@test_class
class bytearray_index_get(l_index_get):
	'buff = bytearray[_]'
	def setup(self):
		super().setup()
		self.buff = bytearray(self.cycles)

@test_class
class bytearray_index_set(l_index_set):
	'bytearray[_] = 0'
	def setup(self):
		super().setup()
		self.buff = bytearray(self.cycles)

@test_class
class tuple_index_get(l_index_get):
	'buff = tuple[_]'
	def setup(self):
		super().setup()
		self.buff = tuple(array.array('I', [1] * self.cycles))

@test_class
class dict_index_get(test):
	'buff = dict[_]'
	def setup(self):
		self.cycles = 1_000_000
		self.buff = {}
		for i in range(self.cycles):
			self.buff[i] = i
	def run(self):
		buff, buff2 = self.buff, 0
		for _ in range(self.cycles):
			buff2 = buff[_]

@test_class
class dict_index_set(test):
	'dict[_] = 0'
	def setup(self):
		self.cycles = 1_000_000
		self.buff = {}
		for i in range(self.cycles):
			self.buff[i] = i
	def run(self):
		buff = self.buff
		for _ in range(self.cycles):
			buff[_] = 0

# String

class string(test):
	def setup(self):
		self.cycles = 100_000
		self.buff = ''

@test_class
class string_concatenate(string):
	'buff += " "'
	def run(self):
		buff = self.buff
		for _ in range(self.cycles):
			buff += ' '

@test_class
class string_join(string):
	'buff.join(" ")'
	def run(self):
		buff = self.buff
		for _ in range(self.cycles):
			buff = buff.join(' ')

@test_class
class string_format(string):
	'buff.format(...)'
	def run(self):
		buff, buff2 = '{0} {1} {2}', ''
		c1, c2 = 2, 3.0
		for _ in range(self.cycles // 10):
			buff2 = buff.format('1', c1, c2)

@test_class
class string_fstring(string):
	'f"{buff} ..."'
	def run(self):
		buff = ''
		c1, c2 = 2, 3.0
		for _ in range(self.cycles // 10):
			buff = f'{buff} {c1} {c2}'

@test_class
class string_cformat(string):
	'"%..." % (...)'
	def run(self):
		buff = ''
		c1, c2 = 2, 3.0
		for _ in range(self.cycles // 10):
			buff = '%s %i %f' % (buff, c1, c2)

# Class

@test_class
class class_attribute(test):
	'class.attribute = 0'
	class a:
		pass
	def setup(self):
		self.cycles = 1_000_000
		self.buff = self.a()
		self.buff._attribute = 0
	def run(self):
		buff = self.buff
		for _ in range(self.cycles):
			buff._attribute = 0

@test_class
class class_slots_attribute(test):
	'class.attribute = 0 (with __slots__)'
	class a:
		__slots__ = ('_attribute',)
	def setup(self):
		self.cycles = 1_000_000
		self.buff = self.a()
		self.buff._attribute = 0
	def run(self):
		buff = self.buff
		for _ in range(self.cycles):
			buff._attribute = 0

# Variable

@test_class
class assingment_multiple_lines(test):
	'a = _; b = _'
	def setup(self):
		self.cycles = 10_000_000
	def run(self):
		a = 0
		b = 0
		for _ in range(self.cycles):
			a = _
			b = _

@test_class
class assingment_one_line(test):
	'a, b = _, _'
	def setup(self):
		self.cycles = 10_000_000
	def run(self):
		a, b = 0, 1
		for _ in range(self.cycles):
			a, b = _, _

@test_class
class variables_self(test):
	'self.a += 1'
	def setup(self):
		self.cycles = 10_000_000
		self.a = 0
	def run(self):
		for _ in range(self.cycles):
			self.a += 1

@test_class
class variables_local(test):
	'a = self.a; a += 1'
	def setup(self):
		self.cycles = 10_000_000
		self.a = 0
	def run(self):
		a = self.a
		for _ in range(self.cycles):
			a += 1

# Spetial cases

@test_class
class synthetic(test):
	'synthetic'
	class Context:
		__slots__ = ('registers', 'breakpoints')
		class Registers:
			__slots__ = ('A', 'B', 'C', 'D', 'E', 'F', 'H', 'L', 'I', 'R', 'IX', 'IY', 'SP', 'PC')
			def __init__(self):
				self.A: int = 0
				self.B: int = 0
				self.C: int = 0
				self.D: int = 0
				self.E: int = 0
				self.F: int = 0
				self.H: int = 0
				self.L: int = 0
				self.I: int = 0
				self.R: int = 0
				self.IX: int = 0
				self.IY: int = 0
				self.SP: int = 0
				self.PC: int = 0
			def __str__(self):
				return 'A={0.A:04x} B={0.B:04x} C={0.C:04x} D={0.D:04x} E={0.E:04x} F={0.F:04x} H={0.H:04x} L={0.L:04x} I={0.I:04x} R={0.R:04x} IX={0.IX:04x} IY={0.IY:04x} SP={0.SP:04x} PC={0.PC:04x}'.format(self)
		class Breakpoint:
			__slots__ = ('address', 'enabled')
			def __init__(self):
				self.address: int = 0
				self.address_end: int = 0
				self.enabled: bool = False
			def is_triggered(self, address :int):
				return self.address <= address <= self.address_end
		def __init__(self):
			self.registers: self.Registers = self.Registers()
			self.breakpoints: List[self.Breakpoint] = []
		def next_instruction(self, pc_advance: int):
			self.registers.PC += pc_advance
	class Instruction:
		__slots__ = ('opcode', 'asm')
		def __init__(self, opcode: int, asm: str):
			'''opcode -- machine opcode
			asm -- assembler mnemonic
			'''
			self.opcode, self.asm = opcode, asm
		def execute(self, context):
			pass
	class mov_a_b(Instruction):
		def __init__(self):
			super().__init__(0xff, 'mov A, B')
		def execute(self, context):
			context.registers.A = context.registers.B
			context.registers.PC
	class inc_b(Instruction):
		def __init__(self):
			super().__init__(0x03, 'inc B')
		def execute(self, context):
			context.registers.B = (context.registers.B + 1) & 0xff
	def setup(self):
		self.cycles = 1_000_000
		self.context = self.Context()
		self.mov_a_b, self.inc_b = self.mov_a_b(), self.inc_b()
	def run(self):
		context, mov_a_b, inc_b = self.context, self.mov_a_b, self.inc_b
		for _ in range(self.cycles):
			mov_a_b.execute(context)
			context.next_instruction(1)
			inc_b.execute(context)
			context.next_instruction(1)
		# print(context.registers)

# --- END TESTS ---

def parse_args():
	global log_level
	parser = argparse.ArgumentParser(description='Test the python interpreter speed')
	parser.add_argument('--csv', action='store_true', help='format results as csv (comma separated values). Do not use with -v option')
	parser.add_argument('--header', action='store_true', help='header for csv')
	parser.add_argument('-l', '--list', action='store_true', help='list availablere tests')
	parser.add_argument('-v', action='count', default=0, help='verbose level: -v, -vv')
	parser.add_argument('-g', '--group', nargs='*', help='run test group')
	parser.add_argument('tests', metavar='[TEST1 [TEST2] ...]', nargs='*', help='space separated tests names. Use --list to list tests')
	ret = parser.parse_args()
	log_level = ret.v
	return ret

available_tests = { x:getattr(sys.modules[__name__], x) for x in dir()
	if isinstance(getattr(sys.modules[__name__], x), type) and issubclass(getattr(sys.modules[__name__], x), test) and  hasattr(getattr(sys.modules[__name__], x), '_is_test') }

args = parse_args()

if args.list:
	# list available tests
	available_tests_names_max_len = max(len(x) for x in available_tests)
	for i, kv in enumerate(available_tests.items()):
		name, func = kv
		print(f'{i+1:02} {name:{available_tests_names_max_len}} {func.__doc__ if func.__doc__ else name}')
else:
	if not (args.csv or args.header):
		print(f'{sys.version}')

	if not args.tests:
		# run all available tests
		tests_names = available_tests.keys()
	else:
		# check for allowable tests
		tests_names, wrong_names = [], []
		for _ in args.tests:
			if _.isdigit():
				if int(_) > 0 and int(_) <= len(available_tests):
					tests_names.append(tuple(available_tests.keys())[int(_) - 1])
				else:
					wrong_names.append(_)
			elif _ not in available_tests:
				wrong_names.append(_)
			else:
				tests_names.append(_)
		if wrong_names:
			print(f'Unknown tests: {", ".join(wrong_names)}')
			print('Use --list to list tests')
			sys.exit(1)

	if args.group:
		tests_names = list(filter(lambda x: any(x.startswith(xx+'_') for xx in args.group), tests_names))
		# tests_names = [ _ for _ in tests_names if _.startswith(args.group+'_') ]

	# run tests
	def run_test(test_class, tests_count=7):
		'runs one test for several times'
		if args.csv:
			print(f'{sys.implementation.name} {python_version()}{delimiter}{test_class.__name__}{delimiter}', end='')
		else:
			print(f'{test_class.__name__:{tests_names_max_len}}{delimiter}', end='\n' if log_level > 0 else '', flush=True)
		time_results = [] # tests time measurements
		for _ in range(tests_count):
			if log_level > 0:
				print(f'\ttest: {_+1}')
			# prepare the test
			tc = test_class()
			tc.setup()
			# run the test with time measurement
			t = time.process_time()
			tc.run()
			elapsed_time = time.process_time() - t
			time_results.append(elapsed_time)
		# tests done # process the time measurements
		if args.csv:
			print(f'{statistics.mean(time_results):1.3}{delimiter}{min(time_results):1.3}{delimiter}{max(time_results):1.3}'
				f'{delimiter}{max(time_results)-min(time_results):1.3}')
		else:
			print(f'avg={statistics.mean(time_results):1.3}{delimiter}min={min(time_results):1.3}{delimiter}max={max(time_results):1.3}'
				f'{delimiter}delta={((max(time_results)-min(time_results))/max(time_results))*100:1.3}% ({max(time_results)-min(time_results):1.3})')

	tests_names_max_len = max(len(x) for x in tests_names)
	delimiter = ',' if args.csv or args.header else ' '
	if args.header:
		print(f'implementation{delimiter}name{delimiter}avg{delimiter}min{delimiter}max{delimiter}delta')
	else:
		for _ in tests_names:
			run_test(available_tests[_])
