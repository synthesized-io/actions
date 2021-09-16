#! /usr/bin/env python3
"""Test file splitter"""
import argparse
import glob
import os
import random

parser = argparse.ArgumentParser(description='Randomly Split files into unique sections. Uses the Git SHA as a seed')
parser.add_argument('--index', metavar='i', type=int, required=True,
                    help='The current processes unqiue index. 0 <= i <= N. When set to 0 returns all files.')
parser.add_argument('--total', metavar='N', type=int, required=True,
                    help='The total number of sections that are being split.')
parser.add_argument('--seed', metavar='seed', type=str, required=False, default=None,
                    help='A random seed used to initialise the splitting. Defaults to GITHUB_SHA.')

args = parser.parse_args()

i = args.index
N = args.total
seed = args.seed if args.seed is not None else os.environ.get('GITHUB_SHA', 'just a random seed')
files = [f for f in glob.glob('tests*/**/test_*.py', recursive=True) if 'metadata' not in f]
random.seed(seed)
random.shuffle(files)

if i == 0:
    section = files
else:
    section = [f for n, f in enumerate(files) if n % (N) == i - 1]

for f in section:
    print(f)
