#!/usr/bin/env python3

import sys
from hashlib import sha256
import csv

encoding = 'utf-8'

if len(sys.argv) != 2:
	exit("Usage: ./hash_it.py <input_filename>")

with open(sys.argv[1], newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|', skipinitialspace=True)
	out = []
	for row in spamreader:
		# print(row)
		out_row = []
		for s in row:
			h = sha256(bytes(s, encoding=encoding)).hexdigest()
			out_row.append(h)
		out.append(out_row)

# print(out)

with open('hashed.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for r in out:
    	writer.writerow(r)