#!/usr/bin/env python3

import sys
from hashlib import sha256
import csv
import random
import string
from time import time

encoding = 'utf-8'
area_codes = ['757', '607', '331']
done = False
cap = list(string.ascii_uppercase)
lower = list(string.ascii_lowercase)

if len(sys.argv) != 2:
	exit("Usage: ./hash_it.py <input_filename>")

with open(sys.argv[1], newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|', skipinitialspace=True)
	start = time()
	voter = 1
	for row in reader:
		print(f"THIS IS VOTER: {voter}")
		hashed_phone = row[0]
		print("Breaking Phone #: ", hashed_phone)

		#insert your code here
		flag = 0
		for j in area_codes:
			if flag == 0:
				for i in range(10000000):
					g_str = j + str(i)
					g = bytes(g_str, encoding=encoding)
					h_code = sha256(g).hexdigest()
					if h_code == hashed_phone:
						print("phone_number:", g_str)
						flag = 1
						break;
		hashed_vote = row[3]
		print("Breaking Vote: ", hashed_vote)
		for i in ['Red', 'Blue']:

			g = bytes(i, encoding=encoding)
			h_code = sha256(g).hexdigest()
			if h_code == hashed_vote:
				print("vote:", i)
		voter += 1
	end = time()
	print("Total time: ", end-start)
		# first_name = row[1]
		# print("Breaking First Name:", first_name)


		# print(cap, lower)
		# fname = ''
		# for i in cap:
		# 	fname = i

		