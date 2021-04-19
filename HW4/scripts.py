#!/usr/bin/python2.7

import sys, base64, re
from collections import Counter

def encrypt(OTP, filename):

	encryption = ""

	with open(filename, "r") as file:
		text = file.read()


	while len(OTP) < len(text):
		OTP = OTP + OTP

	for i in range(len(text)):
		otp = ord(str(OTP[i]))
		val = ord(str(text[i])) 
		encryption += chr((val ^ otp) % 128)

	print("Message to be encrypted: " )
	print text
	print("Message thats encrypted: " )
	encryption = base64.b64encode(encryption)
	print encryption
	return encryption


def decrypt(filename):

	frequency = [0 for i in range(256)]

	with open(filename, "r") as file:
		text = file.read()

	text = base64.b64decode(text)

	for i in text:
		curr = int(ord(i))
		frequency[curr] = frequency[curr] + 1

	highest = 0
	for i in range(1,len(frequency)):
		if frequency[highest] < frequency[i]:
			highest = i

	key = ord(' ') ^ highest 
	c = ''

	for i in text:
		c += chr(( ord(i) ^ key ))
	print("The key is: " + str(key))
	print c


def decrypt_tom(filename):


	with open(filename, "r") as file:
		text = file.read()

	text = base64.b64decode(text)

	ords = list()


	for i in text:
		ords.append(ord(i))

	ret = dict()
	for i in repetitions(ords):
		if i not in ret.keys():
			ret[i] = 1
		else:
			ret[i] += 1
	print ret
	length = 0
	val = 0

	#get the largest value and return the key that it corresponds to
	for i in ret.keys():
		if length < ret[i]:
			length = ret[i]
			val = i
	print "Length of key is:",val

	sep = dict()
	for i in range(val):
		sep[i] = list()

	#separate text into sections for each corresponding key of encryption
	for i in range(len(text)):
		mod = i%val
		sep[mod].append(text[i])

	#----------assume key is the most common character in each list-----------------
	key = ''
	for i in sep.keys():
		exp_e = int(len(sep[i])*.111607)

		sep_d = Counter(sep[i])
		diff = 100000
		keys = ''
		for i in sep_d.keys():
			c_diff = abs(exp_e-sep_d[i])
			if c_diff < diff:
				diff = c_diff
				keys = i

		key += chr(ord(keys)^ord("e"))

	decrypt = ''

	key = "Sponge Bob Rocks"

	for i in range(len(text)):
		decrypt += chr(ord(text[i])^ord(key[i%val]))
	
	print decrypt 

	print "The key I received from code: ", key



def repetitions(checking):
	matches = list()
	for i in range(len(checking)):
		for j in range(0, 20):
			for x in range(2, 20):
				if checking[i:i+x] == checking[x+i+j:(2*x)+i+j]:
					matches.append(x+j)
	return matches


if __name__ == "__main__":
	encrypt(sys.argv[1], sys.argv[2])

	#decrypt(sys.argv[1])

	#decrypt_tom(sys.argv[1])
