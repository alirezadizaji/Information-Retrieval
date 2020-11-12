import time

import dill
from bitarray import bitarray
from sys import getsizeof
import nltk
import os
from collections import defaultdict
import pickle

"""
bitarray has 64 Byte overhead for initialization. 
while raw python list has 56 Byte.for each new entry
0.25 Byte and 1 Byte would be added to memory usage of
bit array and raw python list respectively.
"""


def load_index(path):
    if not os.path.isfile(path):
        raise Exception('INVALID PATH')
    with open(path, "rb") as f:
        index = dill.load(f)
        f.close()
        return {'path': path, 'index': index}

def save_index(idx_info):
    path = idx_info['path'][:-4]

    with open("{}_compressed.pkl".format(path), "wb") as f:
        dill.dump(idx_info['index'], f)
        f.close()

def create_distance_index(index):
    for term in index.keys():
        for docid in index[term].keys():
            pl = index[term][docid]
            length = len(pl)
            distance_pl = [pl[i] if i == 0 else pl[i] - pl[i-1]
                           for i in range(length)]
            index[term][docid] = distance_pl

def decode_distance_index(index):
    for term in index.keys():
        for docid in index[term].keys():
            pl = index[term][docid]
            length = len(pl)
            new_pl = [pl[0]]
            for i in range(1, length):
                element = new_pl[-1] + pl[i]
                new_pl.append(element)
            del pl
            index[term][docid] = new_pl



def dec_to_seven_bit(num):
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
    if num == 0:
        return bitarray("10000000")
    res = bitarray()
    while num > 0:
        num, r = divmod(num, 128)
        res += dec_to_seven_bit(r)
        res.append( len(res)<8 )
    return res[::-1]

def variable_byte_decoder(bitarr):
    size = len(bitarr)
    i, j = 0, 8
    l = []
    while i < size:
        slice = ""
        for j in range(i, size, 8):
            slice += bitarr[j+1:j+8]
            if bitarr[j]:
                j+=8
                break
        if slice != "":
            num = int(slice, 2)
            l.append(num)
        i = j
    return l


def gamma_code_encoder(num):
    binary = dec_to_bin(num)
    length = "1"*( len(binary)-1 ) + "0"
    length = bitarray(length)
    gamma = bitarray(binary[1:])
    return length + gamma

def gamma_code_decoder(bitarr):
    pass

def compress(index, type):
    new_index = defaultdict(list)
    for term in index.keys():
        for docid in index[term].keys():
            pl = index[term][docid]
            res = bitarray()
            for num in pl:
                if type == "vb":
                    res += variable_byte_encoder(num)
                elif type == "gc":
                    res += gamma_code_encoder(num)
                else:
                    print("INVALID TYPE")
                    return
            new_index[term].append((docid, res))
    size = getsizeof(index)
    new_size = getsizeof(new_index)
    print("memory usage origin posting list: {} B, {} KB, {} MB".format(size, size/(2**10), size/(2**20)) )
    print("memory usage modified one: {} B, {} KB, {} MB".format(new_size, new_size/(2**10), new_size/(2**20)) )
    return new_index

def decompress(index, type):
    new_index = defaultdict(lambda : defaultdict(list))
    for term in index.keys():
        for docid, val in index[term]:
            val = str(val)[10:-2] #extracting bit values from bitarray as String
            if type == "vb":
                l = variable_byte_decoder(val)
            elif type == "gc":
                l = gamma_code_decoder(val)
            else:
                print("INVALID TYPE")
                return
            new_index[term][docid] = l
    decode_distance_index(new_index)
    return new_index



"""      compressing       """
path = "eng_doc_positional.pkl"
type = "vb"
info = load_index(path)
idx = info['index']
create_distance_index(idx)
info['index'] = compress(idx, type)
save_index(info)

"""       decompressing     """
path = "{}_compressed.pkl".format(path[:-4])
compressed = load_index(path)['index']
new_index = decompress(compressed, type)
