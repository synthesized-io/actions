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

file_map = {
    "tests/common/test_annotations.py": 2,
    "tests/test_basic.py": 3,
    "tests/insight/test_latent.py": 4,
    "tests/test_basic_synthetic.py": 5,
    "tests/test_export_model.py": 6,
    "tests/fairness/test_bias_mitigator.py": 7,
    "tests/complex/test_multi_table.py": 8,
    "tests/test_dp_synthetic.py": 8,
    "tests/common/test_data_imputer.py": 7,
    "tests/testing/plotting/test_plotting.py": 6,
}
imap = dict()

for fkey, item in file_map.items():
    if item not in imap:
        imap[item] = [fkey]
    else:
        imap[item].append(fkey)

files = [f for f in glob.glob('tests*/**/test_*.py', recursive=True) if 'metadata' not in f and f not in file_map]
random.seed(seed)
random.shuffle(files)

if i == 0:
    section = files + [f for f in file_map.keys()]
else:
    section = [f for n, f in enumerate(files) if n % (N) == i - 1] + imap.get(i, [])

if i == 1: 
    section = section + [f for f in glob.glob('tests*/**/test_*.py', recursive=True) if 'metadata' in f]

for f in section:
    print(f)
