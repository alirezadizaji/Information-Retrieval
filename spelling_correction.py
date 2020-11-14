import os
from collections import defaultdict

import dill
import numpy as np
import nltk

def load_bigram(path):
    if not os.path.isfile(path):
        raise Exception('INVALID PATH')
    with open(path, "rb") as f:
        index = dill.load(f)
        f.close()
        return index

#reference: https://www.geeksforgeeks.org/spelling-correction-using-k-gram-overlap/
def jaccard_dist_type1(q, w, idx):
    A = len(bigram(q))
    B = len(bigram(w))
    AB = 0
    for k, v in idx.items():
        for vocab in v:
            AB += 1 if w == vocab else 0
    A_B = A + B - AB
    return (AB) / (A_B)

#reference: https://python.gotrained.com/nltk-edit-distance-jaccard-distance/#Jaccard_Distance
def jaccard_dist_type2(q, w):
    A = set(q)
    B = set(w)
    A_B = len(A.union(B))
    AB = len(A.intersection(B))
    return AB / A_B


def bigram(w):
    length = len(w)
    return [w[i:i+2] for i in range(length-1)]

def spell_correction(query, bg_idx, type1=True):
    jacc_dist = defaultdict(int)
    ans = [''] * len(query)

    for i, w in enumerate(query):
        bgs = bigram(w)
        ext_idx = {k: bg_idx[k] for k in bgs if k in bg_idx.keys()}
        words = []
        for v in ext_idx.values():
            words.extend(v)

        bag_of_words = set(words)
        if w in bag_of_words:
            ans[i] = w
            continue

        maximum = 0
        while len(bag_of_words) > 0:
            k = bag_of_words.pop()
            jacc_dist[w, k] = jaccard_dist_type1(w, k, ext_idx) if type1 else jaccard_dist_type2(w, k)
            maximum = max(jacc_dist[w, k], maximum)
            ans[i] = k if jacc_dist[w, k] == maximum else ans[i]
    return ans

def edit_distance(w1, w2):
    l1 = len(w1)
    l2 = len(w2)
    dist_mtx = np.zeros(shape=(l1 + 1, l2 + 1), dtype=np.uint8)
    for j in range(l2 + 1):
        dist_mtx[0, j] = j
    for i in range(l1 + 1):
        dist_mtx[i, 0] = i

    for i in range(l1):
        for j in range(l2):
            val1 = dist_mtx[i, j + 1] + 1
            val2 = dist_mtx[i + 1, j] + 1
            val3 = (1 if w1[i] != w2[j] else 0) + dist_mtx[i, j]
            dist_mtx[i + 1, j + 1] = min(val1, val2, val3)
    return dist_mtx[l1, l2]

