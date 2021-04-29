#!/usr/bin/python2.7

import random
import time
from mr import is_probable_prime as is_prime

def int_to_bin(i):
    o = '{0:08b}'.format(i)
    o = (8 - (len(o) % 8)) * '0' + o
    return o

def bin_to_int(b):
    return int(b,2)

def str_to_bin(s):
    o = ''
    for i in s:
        o += '{0:08b}'.format(ord(i))
    return o

def bin_to_str(b):
    l = [b[i:i+8] for i in xrange(0,len(b),8)]
    o = ''
    for i in l:
        o+=chr(int(i,2))
    return o

def egcd(a, b): # can be used to test if numbers are co-primes
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
        #if g==1, the numbers are co-prime

def modinv(a, m):
    #returns multiplicative modular inverse of a in mod m
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

class lfsr:
    # Class implementing linear feedback shift register. Please note that it operates
    # with binary strings, strings of '0's and '1's.
    taps = []
    def __init__(self, taps):
    # Receives a list of taps. Taps are the bit positions that are XOR-ed
    #together and provided to the input of lfsr

        self.register = '1111111111111111'
        # initial state of lfsr
        self.taps = taps

    def clock(self, i='0'):
    #Receives input bit and simulates one cycle
    #This include xoring, shifting, updating input bit and returning output
    #input bit must be XOR-ed with the taps!!

    ## -- Implement me -- ##
        xor = list()
        m = 0
        for j in self.taps:
            if m == 0:
                curr = int(self.register[j])
            else:
                curr = curr ^ int(self.register[j])
            m += 1

        new = str(curr^int(i))

        leaving = self.register[len(self.register)-1]

        self.register = new + self.register[:len(self.register)-1]

        return str(int(leaving)) #returns output bit

    def seed(self, s):
    # This function seeds the lfsr by feeding all bits from s into input of
    # lfsr, output is ignored
        for i in s:
            o = self.clock(i)

    def gen(self,n,skip=0):
    # This function clocks lfsr 'skip' number of cycles ignoring output,
    # then clocks 'n' cycles more and records the output. Then returns
    # the recorded output. This is used as hash or pad
        for x in xrange(skip):
            self.clock()
        out = ''
        for x in xrange(n):
            out += self.clock()
        return out

def H(inp):
    # Hash function, it must initialize a new lfsr, seed it with the inp binary string
    # skip and read the required number of lfsr output bits, returns binary string

    ## -- Implement me -- ##

    # Example: H(int_to_bin(0)) -> '10111000111111111111111000110001010010000101011101001100'
    # Example: H('0') -> '01010101010001110111000111111111111111000110001010010000'
    # Example: H(int_to_bin(777)) -> '00010101011001100111111100110111101011001111001101011001'
    l = lfsr([2,4,5,7,11,14])
    l.seed(inp)
    return l.gen(56, 1000)

def enc_pad(m,p):
    # encrypt message m with pad p, return binary string
    o = ''

    ## -- Implement me -- ##
    for i in range(len(m)):
        o += str(int(m[i])^int(p[i]))

    return o

def GenRSA():
    # Function to generate RSA keys. Use the Euler's totient function (phi)
    # As we discussed in lectures. Function must: 1) seed python's random number
    # generator with time.time() 2) Generate RSA primes by keeping generating
    # random integers of size 512 bit using the random.getrandbits(512) and testing
    # whether they are prime or not using the is_prime function until both primes found.
    # 3) compute phi 4) find e that is coprime to phi. Start from e=3 and keep
    # incrementing until you find a suitable one. 4) derive d 5) return tuple (n,e,d)
    # n - public modulo, e - public exponent, d - private exponent

    random.seed(time.time())

    ## -- Implement me -- ##
    p = random.getrandbits(512)
    while not is_prime(p):
        p = random.getrandbits(512)


    q = random.getrandbits(512)
    while not is_prime(q):
        q = random.getrandbits(512)

    n = p*q

    phi = (p-1)*(q-1)

    e = 3
    temp = egcd(e, phi)
    while e < phi and temp[0] != 1:
        e += 1
        temp = egcd(e, phi)

    d = modinv(e, phi)


    return (n,e,d)

if __name__ == "__main__":

    (n,e,d) = GenRSA()
    s = "Daniel Quiroga dquiroga@email.wm.edu"
    bs = str_to_bin(s)
    ints = bin_to_int(bs)

    message = pow(ints,e,n)
    message = int_to_bin(message)
    print("Signature of the  message: " + message)

#------------How to verify signature-----------------
    other_party = message

    other_party = bin_to_int(other_party)
    integer = pow(other_party,d,n)
    binary = int_to_bin(integer)
    original_message = bin_to_str(binary)
    print("\n\nOriginal Message: "+original_message)

    #----------------P1-------------------------
    # l = lfsr([2,4,5,7,11,14])
    # l.seed(int_to_bin(4321))
    # print(l.gen(10,1000))
    # l = lfsr([2,4,5,7,11,14])
    # l.seed(int_to_bin(1234))
    # print(l.gen(10,2000))

    #--------------------P2 -----------------
    # print(H(str_to_bin('My name is Bart Simpson and I like krusty burgers')))
    # print(H(int_to_bin(0)))
    # print(H('0'))
    # print(H(int_to_bin(777)))
    # print(H(str_to_bin('My name is Daniel Quiroga and I like crispy tenders')))


    #----------------------P3---------------------------------------
    # s = "Hello, my name is Bobby Hill"
    # bs = str_to_bin(s)
    # print(bs)
    # print(" ")
    # l = lfsr([2,4,5,7,11,14])
    # l.seed(int_to_bin(77))
    # pad = l.gen(len(bs), 1000)
    # print(pad)
    # print(" ")
    # cipher = enc_pad(bs,pad)
    # print(cipher)
    # print(" ")
    # print(bin_to_str(cipher))
    # print(" ")
    # print(bin_to_str(enc_pad(cipher,pad)))

    # s = "Hello, my name is Daniel Quiroga"
    # bs = str_to_bin(s)
    # print(bs)
    # print(" ")
    # l = lfsr([2,4,5,7,11,14])
    # l.seed(int_to_bin(77))
    # pad = l.gen(len(bs), 1000)
    # print(pad)
    # print(" ")
    # cipher = enc_pad(bs,pad)
    # print(cipher)
    # print(" ")
    # print(bin_to_str(cipher))
    # print(" ")
    # print(bin_to_str(enc_pad(cipher,pad)))


    #---------------------P4-----------------------
    # (n,e,d) = GenRSA()
    # print((n,e,d))

    # t = 100
    # c = pow(t,e,n)
    # print(pow(c,d,n) == t)