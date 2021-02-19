#!/usr/bin/env python3

import argparse
from pathlib import Path
import seaborn as sns
import pandas as pd


def parse_args():
	global log_level
	parser = argparse.ArgumentParser(description='Converts .csv files to graph and saves to .png files')
	parser.add_argument('-v', action='count', default=0, help='verbose level: -v, -vv')
	parser.add_argument('tests', metavar='[TEST1 [TEST2] ...]', nargs='*', help='space separated tests names. Use --list to list tests')
	ret = parser.parse_args()
	log_level = ret.v
	return ret

args = parse_args()

for test in args.tests:
	test_out = Path(test).with_suffix('.png')
	if args.v > 0:
		print(f'\topen {test}')
	d = pd.read_csv(test, header=0)
	g = sns.catplot(x='name', y='avg', hue='implementation', data=d, kind='bar', log=True)
	g.ax.set_xticklabels(g.ax.get_xticklabels(),rotation=90)
	g.ax.set_ylabel('time, low - better')
	if args.v > 0:
		print(f'\tsave {test_out}')
	g.savefig(test_out)
