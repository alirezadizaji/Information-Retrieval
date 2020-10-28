from bitarray import bitarray
from sys import getsizeof
"""
bitarray has 64 Byte overhead for initialization. 
while raw python list has 56 Byte.for each new entry
0.25 Byte and 1 Byte would be added to memory usage of
bit array and raw python list respectively.
"""

def seven_bit(num):
    res = bitarray('0000000')
    idx = 0
    while num > 0:
        num, r = divmod(num, 2)
        res[idx] = r
        idx += 1
    return res

def dec_to_bin(num):
    return bin(num)[2:]

def variable_byte_encoder(num):
    res = bitarray()
    while num > 0:
        num, r = divmod(num, 128)
        res += seven_bit(r)
        res.append( len(res)<8 )
    return res[::-1]

def gamma_code_encoder(num):
    binary = dec_to_bin(num)
    length = "1"*( len(binary)-1 ) + "0"
    length = bitarray(length)
    gamma = bitarray(binary[1:])
    return length + gamma

def encode_posting(posting, type):
    res = bitarray()
    for num in posting:
        if type == "vb":
            res += variable_byte_encoder(num)
        elif type == "gc":
            res += gamma_code_encoder(num)
    size = getsizeof(posting)
    size2 = getsizeof(res)
    print("memory usage origin posting list: {} B, {} KB, {} MB".format(size, size/(2**10), size/(2**20)) )
    print("memory usage modified one: {} B, {} KB, {} MB".format(size2, size2/(2**10), size/(2**20)) )
    return res
