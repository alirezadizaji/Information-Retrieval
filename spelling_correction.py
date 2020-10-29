import numpy as np
import nltk

def jacc_type1(w1, w2, posting):
    w1_repu = {}
    w2_repu = {}
    for k, v in posting.items():
        for w in v:
            w1_repu[k] += 1 if w == w1 else 0
            w2_repu[k] += 1 if w == w2 else 0
    A = sum(w1_repu.values())
    B = sum(w2_repu.values())
    A_B = 0
    for k in posting.keys():
        A_B += min(w1_repu[k], w2_repu[k])
    return (A_B) / (A + B - A_B)

def jacc_type2(w1, w2):
    return nltk.jaccard_distance(w1, w2)

def spell_correction(query, bg_posting, type1=True):
    jacc_dist = {}
    ans = [''] * len(query)

    for i, w in enumerate(query):
        bgs = nltk.bigrams(w)
        ext_posting = {k: bg_posting[k] for k in bgs if k in bg_posting.keys()}
        words = []
        for k, v in ext_posting.items():
            words.extend(v)

        bag_of_words = set(words)
        if w in bag_of_words:
            ans[i] = w
            break

        maximum = 0
        while len(bag_of_words) >= 0:
            k = bag_of_words.pop()
            jacc_dist[w, k] = jacc_type1(w,k,ext_posting) if type1 else jacc_type2(w,k)
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

