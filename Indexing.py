import json
import os
import pprint
import dill as dill
import pandas as pd
from collections import defaultdict
# ------------------------------------#
# import English_preproccess.preproccess as ep
# import Presian_preproccess.preproccess as pp
import math
import numpy as np


# ---------------------------------------------------------Eng Ted Talk------------------------------------------------#
eng_title_posting_list = defaultdict(lambda: defaultdict(list))
eng_document_posting_list = defaultdict(lambda: defaultdict(list))
eng_title_bigram_list = defaultdict(list)
eng_document_bigram_list = defaultdict(list)
eng_ids = []
eng_total_documents = 0


# for t, d in zip(titles, descriptions):
#     print(t, "\n", d)


def eng_create_index():
    global eng_title_posting_list, eng_document_posting_list, eng_total_documents

    csv_data = pd.read_csv("test.csv")
    titles = csv_data['title']
    descriptions = csv_data['description']
    id = 0
    for title, description in zip(titles, descriptions):
        title_words = title.split(" ")
        description_words = description.split(" ")
        for i, t in enumerate(title_words):
            eng_title_posting_list[t][id].append(i + 1)
        for i, d in enumerate(description_words):
            eng_document_posting_list[d][id].append(i + 1)
        eng_ids.append(id)
        eng_total_documents += 1
        id += 1
    # print(eng_document_posting_list)
    return


def eng_delete_index(doc_id):
    global eng_title_posting_list, eng_document_posting_list

    for k in eng_title_posting_list.keys():
        if doc_id in eng_title_posting_list[k].keys():
            # print(title_posting_list[k][doc_id])
            del eng_title_posting_list[k][doc_id]
    for k in eng_document_posting_list.keys():
        if doc_id in eng_document_posting_list[k].keys():
            # print(document_posting_list[k][doc_id])
            del eng_document_posting_list[k][doc_id]
    return


def eng_add_index(path):
    global eng_title_posting_list, eng_document_posting_list

    data = pd.read_csv(path)
    titles = data['title']
    descriptions = data['description']
    id = eng_ids[-1] + 1
    eng_ids.append(id)
    for title, description in zip(titles, descriptions):
        # print(id, "    ", title, "  ", document)
        title_words = title.split(" ")
        description_words = description.split(" ")
        for i, t in enumerate(title_words):
            eng_title_posting_list[t][id].append(i + 1)
        for i, d in enumerate(description_words):
            eng_document_posting_list[d][id].append(i + 1)
    return


def eng_get_index(word, field):
    if len(word) < 1:
        print("WORD LENGTH IS ZERO")
        return
    if field == 'TITLE':
        if word not in eng_title_posting_list.keys():
            print("WORD DOES NOT EXIST")
            return
        posting_list = eng_title_posting_list[word]
        pprint.pprint(json.loads(json.dumps(posting_list)))
        return
    elif field == 'TEXT':
        if word not in eng_document_posting_list.keys():
            print("WORD DOES NOT EXIST")
            return
        posting_list = eng_document_posting_list[word]
        pprint.pprint(json.loads(json.dumps(posting_list)))
        return
    return


def eng_load_index():
    global eng_title_posting_list, eng_document_posting_list
    # title
    eng_title_positional = open("eng_title_positional.txt", "rb")
    eng_title_posting_list = dill.load(eng_title_positional)
    eng_title_positional.close()
    # doc
    eng_doc_positional = open("eng_doc_positional.txt", "rb")
    eng_document_posting_list = dill.load(eng_doc_positional)
    eng_doc_positional.close()
    return


def eng_save_index():
    # title
    eng_title_positional = open("eng_title_positional.txt", "wb")
    dill.dump(eng_title_posting_list, eng_title_positional)
    eng_title_positional.close()
    # doc
    eng_doc_positional = open("eng_doc_positional.txt", "wb")
    dill.dump(eng_document_posting_list, eng_doc_positional)
    eng_doc_positional.close()
    return


def eng_create_bigram():
    global eng_title_bigram_list, eng_document_bigram_list
    # title
    for k in eng_title_posting_list.keys():
        for index in range(0, len(k)):
            if index < len(k) - 1:
                bigram = k[index:index + 2]
                eng_title_bigram_list[bigram].append(k)
    # document
    for k in eng_document_posting_list.keys():
        for index in range(0, len(k)):
            if index < len(k) - 1:
                bigram = k[index:index + 2]
                eng_document_bigram_list[bigram].append(k)
    return


def eng_delete_bigram(word, field):
    global eng_title_bigram_list, eng_document_bigram_list

    if field == 'TITLE':
        if len(word) < 1:
            print("WORD LENGTH IS ZERO")
            return
        for k in eng_title_bigram_list.keys():
            if word in eng_title_bigram_list[k]:
                eng_title_bigram_list[k].remove(word)
    elif field == 'TEXT':
        if len(word) < 1:
            print("WORD LENGTH IS ZERO")
            return
        for k in eng_document_bigram_list.keys():
            if word in eng_document_bigram_list[k]:
                eng_document_bigram_list[k].remove(word)
    return


def eng_add_bigram(word, field):
    global eng_title_bigram_list, eng_document_bigram_list

    if field == 'TITLE':
        for index in range(0, len(word)):
            if index < len(word) - 1:
                bigram = word[index:index + 2]
                eng_title_bigram_list[bigram].append(word)
    elif field == 'TEXT':
        for index in range(0, len(word)):
            if index < len(word) - 1:
                bigram = word[index:index + 2]
                eng_document_bigram_list[bigram].append(word)
    return


def eng_get_bigram(bigram, field):
    if len(bigram) < 1:
        print("LENGTH ZERO")
        return
    if field == 'TITLE':
        if bigram not in eng_title_bigram_list.keys():
            print("BIGRAM DOES NOT EXIST")
            return
        print(eng_title_bigram_list[bigram])
        return
    elif field == 'TEXT':
        if bigram not in eng_document_bigram_list.keys():
            print("BIGRAM DOES NOT EXIST")
            return
        print(eng_document_bigram_list[bigram])
        return
    return


def eng_save_bigram():
    # title
    eng_title_bigram = open("eng_title_bigram.txt", "wb")
    dill.dump(eng_title_bigram_list, eng_title_bigram)
    eng_title_bigram.close()
    # doc
    eng_doc_bigram = open("eng_doc_bigram.txt", "wb")
    dill.dump(eng_document_bigram_list, eng_doc_bigram)
    eng_doc_bigram.close()
    return


def eng_load_bigram():
    global eng_title_bigram_list, eng_document_bigram_list
    # title
    eng_title_bigram = open("eng_title_bigram.txt", "rb")
    eng_title_bigram_list = dill.load(eng_title_bigram)
    print(eng_title_bigram_list)
    eng_title_bigram.close()
    # doc
    eng_doc_bigram = open("eng_doc_bigram.txt", "rb")
    eng_document_bigram_list = dill.load(eng_doc_bigram)
    print(eng_document_bigram_list)
    eng_doc_bigram.close()
    return


# -----------------------------------------------------------WIKI------------------------------------------------------#
title_posting_list = defaultdict(lambda: defaultdict(list))
document_posting_list = defaultdict(lambda: defaultdict(list))
title_bigram_list = defaultdict(list)
document_bigram_list = defaultdict(list)
wiki_total_documents = 0
wiki_ids = []


def wiki_create_index():
    global title_posting_list, document_posting_list, wiki_total_documents
    data = pd.read_csv("Presian_preproccess/prepared_persian.csv")
    titles = data['title']
    documents = data['text']
    id = data['id']
    ids = 0
    for doc_id, title, document in zip(id, titles, documents):
        # print(doc_id, "    ", title, "  ", document)
        title_words = title.split(" ")
        document_words = document.split(" ")
        for i, t in enumerate(title_words):
            title_posting_list[t][ids].append(i + 1)
        for i, d in enumerate(document_words):
            document_posting_list[d][ids].append(i + 1)
        wiki_total_documents += 1
        wiki_ids.append(ids)
        ids += 1
    # print(document_posting_list['help'])
    return


def wiki_delete_index(doc_id):
    global title_posting_list, document_posting_list

    for k in title_posting_list.keys():
        if doc_id in title_posting_list[k].keys():
            # print(title_posting_list[k][doc_id])
            del title_posting_list[k][doc_id]
    for k in document_posting_list.keys():
        if doc_id in document_posting_list[k].keys():
            # print(document_posting_list[k][doc_id])
            del document_posting_list[k][doc_id]
    return


def wiki_add_index(path):
    global title_posting_list, document_posting_list
    data = pd.read_csv(path)
    titles = data['title']
    documents = data['text']
    id = data['id']
    ids = wiki_ids[-1] + 1
    wiki_ids.append(ids)
    for v in document_posting_list.values():
        if v.keys().__contains__(id):
            print("Document Already exists")
            return
    for doc_id, title, document in zip(id, titles, documents):
        print(doc_id, "    ", title, "  ", document)
        title_words = title.split(" ")
        document_words = document.split(" ")
        for i, t in enumerate(title_words):
            title_posting_list[t][ids].append(i + 1)
        for i, d in enumerate(document_words):
            title_posting_list[d][ids].append(i + 1)
    print(document_posting_list['help'])
    return


def wiki_get_index(word, field):
    global title_posting_list, document_posting_list
    if len(word) <= 0:
        print("WORD LENGTH IS 0")
        return
    if field == 'TITLE':
        if word not in title_posting_list.keys():
            print("WORD: ", word, "NOT IN THE DICTIONARY")
            return
        posting_list = title_posting_list[word]
        pprint.pprint(json.loads(json.dumps(posting_list)))
        return
    elif field == 'TEXT':
        if word not in document_posting_list.keys():
            print("WORD: ", word, "NOT IN THE DICTIONARY")
            return
        posting_list = document_posting_list[word]
        pprint.pprint(json.loads(json.dumps(posting_list)))
        return


def wiki_load_index():
    global title_posting_list, document_posting_list
    # title
    wiki_title_positional = open("wiki_title_positional.txt", "rb")
    print(title_posting_list)
    title_posting_list = dill.load(wiki_title_positional)
    print(title_posting_list)
    wiki_title_positional.close()
    # doc
    wiki_doc_positional = open("wiki_doc_positional.txt", "rb")
    document_posting_list = dill.load(wiki_doc_positional)
    wiki_doc_positional.close()
    return


def wiki_save_index():
    # title
    wiki_title_positional = open("wiki_title_positional.txt", "wb")
    dill.dump(title_posting_list, wiki_title_positional)
    wiki_title_positional.close()
    # doc
    wiki_doc_positional = open("wiki_doc_positional.txt", "wb")
    dill.dump(document_posting_list, wiki_doc_positional)
    wiki_doc_positional.close()
    return


def wiki_create_bigram():
    global title_bigram_list, document_bigram_list
    # title
    for k in title_posting_list.keys():
        for index in range(0, len(k)):
            if index < len(k) - 1:
                bigram = k[index:index + 2]
                title_bigram_list[bigram].append(k)
    # document
    for k in document_posting_list.keys():
        for index in range(0, len(k)):
            if index < len(k) - 1:
                bigram = k[index:index + 2]
                document_bigram_list[bigram].append(k)
    return


def wiki_delete_bigram(word, field):
    global title_bigram_list, document_bigram_list
    if field == 'TITLE':
        if len(word) < 1:
            print("WORD LENGTH IS ZERO")
            return
        for k in title_bigram_list.keys():
            if word in title_bigram_list[k]:
                title_bigram_list[k].remove(word)
    elif field == 'TEXT':
        if len(word) < 1:
            print("WORD LENGTH IS ZERO")
            return
        for k in document_bigram_list.keys():
            if word in document_bigram_list[k]:
                document_bigram_list[k].remove(word)
    return


def wiki_add_bigram(word, field):
    global title_bigram_list, document_bigram_list

    if field == 'TITLE':
        for index in range(0, len(word)):
            if index < len(word) - 1:
                bigram = word[index:index + 2]
                title_bigram_list[bigram].append(word)
    elif field == 'TEXT':
        for index in range(0, len(word)):
            if index < len(word) - 1:
                bigram = word[index:index + 2]
                document_bigram_list[bigram].append(word)
    return


def wiki_get_bigram(bigram, field):
    if len(bigram) < 1:
        print("LENGTH ZERO")
        return
    if field == 'TITLE':
        if bigram not in title_bigram_list.keys():
            print("BIGRAM DOES NOT EXIST")
            return
        print(title_bigram_list[bigram])
        return
    elif field == 'TEXT':
        if bigram not in document_bigram_list.keys():
            print("BIGRAM DOES NOT EXIST")
            return
        print(document_bigram_list[bigram])
        return


def wiki_save_bigram():
    # title
    wiki_title_bigram = open("wiki_title_bigram.txt", "wb")
    dill.dump(title_bigram_list, wiki_title_bigram)
    wiki_title_bigram.close()
    # doc
    wiki_doc_bigram = open("wiki_doc_bigram.txt", "wb")
    dill.dump(document_bigram_list, wiki_doc_bigram)
    wiki_doc_bigram.close()
    return


def wiki_load_bigram():
    global title_bigram_list, document_bigram_list
    # title
    wiki_title_bigram = open("wiki_title_bigram.txt", "rb")
    title_bigram_list = dill.load(wiki_title_bigram)
    print(title_bigram_list)
    wiki_title_bigram.close()
    # doc
    wiki_doc_bigram = open("wiki_doc_bigram.txt", "rb")
    document_bigram_list = dill.load(wiki_doc_bigram)
    print(document_bigram_list)
    wiki_doc_bigram.close()
    return


eng_create_index()
print(eng_title_posting_list)
print(eng_document_posting_list)
# eng_get_index('salam', 'TITLE')
# eng_delete_index(0)
# eng_get_index('salam', 'TITLE')
# eng_create_bigram()
# print(eng_title_bigram_list)
# print(eng_document_bigram_list)
# eng_get_bigram('sa', 'TITLE')
# eng_delete_bigram('salam', 'TITLE')
# print(eng_title_bigram_list)
# print(eng_document_bigram_list)
# eng_add_bigram('al', 'TITLE')
# print(eng_title_bigram_list)
# ------------------------------------------------------------- retrieval --------------------------------------------#


DOC_TYPE = 'Eng'
ret_text_posting_list = defaultdict(lambda: defaultdict(list))
ret_title_posting_list = defaultdict(lambda: defaultdict(list))
tot_documents = 0


def calc_tf(tf):
    if tf == 0:
        return 0
    else:
        return 1 + math.log(tf, 10)


def calc_idf(df):
    return math.log((tot_documents / (df + 1)), 10)


def create_title_tf_table():
    global ret_title_posting_list, title_terms, title_term_to_number
    # title_terms = list(ret_title_posting_list.keys())
    # title_term_to_number = {t: i for i, t in enumerate(title_terms)}
    tf = np.zeros((tot_documents, len(title_terms)))
    for t in ret_title_posting_list.keys():
        for d in ret_title_posting_list[t].keys():
            tf[d][title_term_to_number[t]] = calc_tf(len(ret_title_posting_list[t][d]))
    return tf


def create_text_tf_table():
    global ret_text_posting_list, text_terms, text_term_to_number
    # text_terms = list(ret_text_posting_list.keys())
    # text_term_to_number = {t: i for i, t in enumerate(text_terms)}
    tf = np.zeros((tot_documents, len(text_terms)))
    for t in ret_text_posting_list.keys():
        for d in ret_text_posting_list[t].keys():
            tf[d][text_term_to_number[t]] = calc_tf(len(ret_text_posting_list[t][d]))
    return tf


def create_title_idf():
    idf = [0] * len(title_terms)
    for t in ret_title_posting_list.keys():
        idf[title_term_to_number[t]] = calc_idf(len(ret_title_posting_list[t]))
    return idf


def create_text_idf():
    idf = [0] * len(text_terms)
    for t in ret_text_posting_list.keys():
        idf[text_term_to_number[t]] = calc_idf(len(ret_text_posting_list[t]))
    return idf


def calc_title_weights():
    global title_tf, title_idf

    for d in range(title_tf.shape[0]):
        w = 0
        for t in range(title_tf.shape[1]):
            title_tf[d][t] = title_tf[d][t] * title_idf[t]
            w += title_tf[d][t] ** 2
        w = math.sqrt(w)
        for t in range(title_tf.shape[1]):
            title_tf[d][t] = title_tf[d][t] / w

    return title_tf


def calc_text_weights():
    global text_tf, text_idf

    for d in range(text_tf.shape[0]):
        w = 0
        for t in range(text_tf.shape[1]):
            text_tf[d][t] = text_tf[d][t] * text_idf[t]
            w += text_tf[d][t] ** 2
        w = math.sqrt(w)
        for t in range(text_tf.shape[1]):
            text_tf[d][t] = text_tf[d][t] / w

    return text_tf


def ltc_lnc(header, query):
    global title_weights, text_weights
    # if DOC_TYPE == 'Eng':
    #     query = ep.clean_text(query)
    # else:
    #     query = pp.prepare_text(query)
    query_terms = query.split()
    if header == 'title':
        query_terms_ = [q for q in query_terms if q in ret_title_posting_list.keys()]
        query_ = {i: calc_tf(query_terms_.count(i)) for i in np.unique(query_terms_)}
        w = 0
        for q in query_.keys():
            w += query_[q] ** 2
        w = math.sqrt(w)
        for q in query_.keys():
            query_[q] = query_[q] / w
        scores = [0] * tot_documents
        for d in range(tot_documents):
            for q in query_.keys():
                scores[d] += (title_weights[d][title_term_to_number[q]] * query_[q])
    else:
        query_terms_ = [q for q in query_terms if q in ret_text_posting_list.keys()]
        query_ = {i: calc_tf(query_terms_.count(i)) for i in np.unique(query_terms_)}
        w = 0
        for q in query_.keys():
            w += query_[q] ** 2
        w = math.sqrt(w)
        for q in query_.keys():
            query_[q] = query_[q] / w
        scores = [0] * tot_documents
        for d in range(tot_documents):
            for q in query_.keys():
                scores[d] += (text_weights[d][text_term_to_number[q]] * query_[q])
    return scores


def retrieve_posting_lists():
    global ret_text_posting_list, ret_title_posting_list, tot_documents
    if DOC_TYPE == 'Eng':
        ret_text_posting_list = eng_document_posting_list
        ret_title_posting_list = eng_title_posting_list
        tot_documents = eng_total_documents
    else:
        ret_text_posting_list = document_posting_list
        ret_title_posting_list = title_posting_list
        tot_documents = wiki_total_documents


retrieve_posting_lists()
title_terms = list(ret_title_posting_list.keys())
title_term_to_number = {t: i for i, t in enumerate(title_terms)}
text_terms = list(ret_text_posting_list.keys())
text_term_to_number = {t: i for i, t in enumerate(text_terms)}
title_tf = create_title_tf_table()
text_tf = create_text_tf_table()
title_idf = create_title_idf()
text_idf = create_text_idf()
title_weights = calc_title_weights()
text_weights = calc_text_weights()


def add_scores(title_scores, text_scores):
    id_score_pair = list(enumerate(np.add(title_scores, text_scores)))
    max_ = max(10, len(id_score_pair))
    s = sorted(id_score_pair, key=lambda x: x[1], reverse=True)[:max_]
    return s


def search(query):
    title_scores = ltc_lnc('title', query)
    text_scores = ltc_lnc('text', query)
    best_doc_ids = add_scores(title_scores, text_scores)
    print(best_doc_ids)


print("Enter your query")
search(input())
