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
# eng_title_posting_list = defaultdict(lambda: defaultdict(list))
# eng_document_posting_list = defaultdict(lambda: defaultdict(list))
# eng_title_bigram_list = defaultdict(list)
# eng_document_bigram_list = defaultdict(list)
# eng_ids = []
# eng_total_documents = 0

def eng_create_index(path):
    # global eng_title_posting_list, eng_document_posting_list, eng_total_documents
    eng_title_posting_list = defaultdict(lambda: defaultdict(list))
    eng_document_posting_list = defaultdict(lambda: defaultdict(list))
    eng_ids = []
    eng_total_documents = 0
    csv_data = pd.read_csv(path)
    titles = csv_data['title']
    descriptions = csv_data['description']
    id = 0
    for title, description in zip(titles, descriptions):
        if not str(title) == 'nan' and not str(description) == 'nan':
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
    return eng_title_posting_list, eng_document_posting_list, eng_total_documents


def eng_delete_index(doc_id, eng_title_posting_list, eng_document_posting_list, eng_total_documents):

    # global eng_title_posting_list, eng_document_posting_list

    for k in eng_title_posting_list.keys():
        if doc_id in eng_title_posting_list[k].keys():
            # print(title_posting_list[k][doc_id])
            del eng_title_posting_list[k][doc_id]
    for k in eng_document_posting_list.keys():
        if doc_id in eng_document_posting_list[k].keys():
            # print(document_posting_list[k][doc_id])
            del eng_document_posting_list[k][doc_id]
    # eng_total_documents -= 1
    return eng_title_posting_list, eng_document_posting_list, eng_total_documents


def eng_add_index(path, eng_title_posting_list, eng_document_posting_list, eng_total_documents):
    # global eng_title_posting_list, eng_document_posting_list

    data = pd.read_csv(path)
    titles = data['title']
    descriptions = data['description']
    id = eng_total_documents
    eng_total_documents += 1
    for title, description in zip(titles, descriptions):
        # print(id, "    ", title, "  ", document)
        title_words = title.split(" ")
        description_words = description.split(" ")
        for i, t in enumerate(title_words):
            eng_title_posting_list[t][id].append(i + 1)
        for i, d in enumerate(description_words):
            eng_document_posting_list[d][id].append(i + 1)
    return eng_title_posting_list, eng_document_posting_list, eng_total_documents


def eng_get_index(word, field, eng_title_posting_list, eng_document_posting_list):
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
    # global eng_title_posting_list, eng_document_posting_list
    # title
    eng_title_positional = open("eng_title_positional.txt", "rb")
    eng_title_posting_list = dill.load(eng_title_positional)
    eng_title_positional.close()
    # doc
    eng_doc_positional = open("eng_doc_positional.txt", "rb")
    eng_document_posting_list = dill.load(eng_doc_positional)
    eng_doc_positional.close()
    return eng_title_posting_list, eng_document_posting_list


def eng_save_index(eng_title_posting_list, eng_document_posting_list):
    # title
    print("writing")
    eng_title_positional = open("eng_title_positional.txt", "wb")
    dill.dump(eng_title_posting_list, eng_title_positional)
    eng_title_positional.close()
    # doc
    eng_doc_positional = open("eng_doc_positional.txt", "wb")
    dill.dump(eng_document_posting_list, eng_doc_positional)
    eng_doc_positional.close()
    print("done")
    return


def eng_create_bigram(eng_title_posting_list, eng_document_posting_list):
    # global eng_title_bigram_list, eng_document_bigram_list
    eng_title_bigram_list = defaultdict(list)
    eng_document_bigram_list = defaultdict(list)
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
    return eng_title_bigram_list, eng_document_bigram_list


def eng_delete_bigram(word, field, eng_title_bigram_list, eng_document_bigram_list):
    # global eng_title_bigram_list, eng_document_bigram_list

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
    return eng_title_bigram_list, eng_document_bigram_list


def eng_add_bigram(word, field, eng_title_bigram_list, eng_document_bigram_list):
    # global eng_title_bigram_list, eng_document_bigram_list

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
    return eng_title_bigram_list, eng_document_bigram_list


def eng_get_bigram(bigram, field, eng_title_bigram_list, eng_document_bigram_list):
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


def eng_save_bigram(eng_title_bigram_list, eng_document_bigram_list):
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
    # global eng_title_bigram_list, eng_document_bigram_list
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
    return eng_title_bigram_list, eng_document_bigram_list


# -----------------------------------------------------------WIKI------------------------------------------------------#
# title_posting_list = defaultdict(lambda: defaultdict(list))
# document_posting_list = defaultdict(lambda: defaultdict(list))
# title_bigram_list = defaultdict(list)
# document_bigram_list = defaultdict(list)
# wiki_total_documents = 0
# wiki_ids = []


def wiki_create_index(path):
    # global title_posting_list, document_posting_list, wiki_total_documents
    title_posting_list = defaultdict(lambda: defaultdict(list))
    document_posting_list = defaultdict(lambda: defaultdict(list))
    wiki_total_documents = 0
    data = pd.read_csv(path)
    titles = data['title']
    documents = data['text']
    id = data['id']
    ids = 0
    for doc_id, title, document in zip(id, titles, documents):
        # print(doc_id, "    ", title, "  ", document)
            print(title)
            title_words = title.split(" ")
            document_words = document.split(" ")
            for i, t in enumerate(title_words):
                title_posting_list[t][ids].append(i + 1)
            for i, d in enumerate(document_words):
                document_posting_list[d][ids].append(i + 1)
            wiki_total_documents += 1
            # wiki_ids.append(ids)
            ids += 1
    # print(document_posting_list['help'])
    return title_posting_list, document_posting_list, wiki_total_documents


def wiki_delete_index(doc_id, title_posting_list, document_posting_list, wiki_total_documents):
    # global title_posting_list, document_posting_list

    for k in title_posting_list.keys():
        if doc_id in title_posting_list[k].keys():
            # print(title_posting_list[k][doc_id])
            del title_posting_list[k][doc_id]
    for k in document_posting_list.keys():
        if doc_id in document_posting_list[k].keys():
            # print(document_posting_list[k][doc_id])
            del document_posting_list[k][doc_id]
    # wiki_total_documents -= 1
    return title_posting_list, document_posting_list, wiki_total_documents


def wiki_add_index(path, title_posting_list, document_posting_list, wiki_total_documents):
    # global title_posting_list, document_posting_list
    data = pd.read_csv(path)
    titles = data['title']
    documents = data['text']
    id = data['id']
    ids = wiki_total_documents
    wiki_total_documents += 1
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
    return title_posting_list, document_posting_list


def wiki_get_index(word, field, title_posting_list, document_posting_list):
    # global title_posting_list, document_posting_list
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
    # global title_posting_list, document_posting_list
    # title
    wiki_title_positional = open("wiki_title_positional.txt", "rb")
    # print(title_posting_list)
    title_posting_list = dill.load(wiki_title_positional)
    # print(title_posting_list)
    wiki_title_positional.close()
    # doc
    wiki_doc_positional = open("wiki_doc_positional.txt", "rb")
    document_posting_list = dill.load(wiki_doc_positional)
    wiki_doc_positional.close()
    return title_posting_list, document_posting_list


def wiki_save_index(title_posting_list, document_posting_list):
    # title
    wiki_title_positional = open("wiki_title_positional.txt", "wb")
    dill.dump(title_posting_list, wiki_title_positional)
    wiki_title_positional.close()
    # doc
    wiki_doc_positional = open("wiki_doc_positional.txt", "wb")
    dill.dump(document_posting_list, wiki_doc_positional)
    wiki_doc_positional.close()
    return


def wiki_create_bigram(title_posting_list, document_posting_list):
    # global title_bigram_list, document_bigram_list
    title_bigram_list = defaultdict(list)
    document_bigram_list = defaultdict(list)
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
    return title_bigram_list, document_bigram_list


def wiki_delete_bigram(word, field, title_bigram_list, document_bigram_list):
    # global title_bigram_list, document_bigram_list
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
    return title_bigram_list, document_bigram_list


def wiki_add_bigram(word, field, title_bigram_list, document_bigram_list):
    # global title_bigram_list, document_bigram_list

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
    return title_bigram_list, document_bigram_list


def wiki_get_bigram(bigram, field, title_bigram_list, document_bigram_list):
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


def wiki_save_bigram(title_bigram_list, document_bigram_list):
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
    # global title_bigram_list, document_bigram_list
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
    return title_bigram_list, document_bigram_list


# eng_create_index()
# print(eng_title_posting_list)
# print(eng_document_posting_list)
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
