import json
import os
import pprint
import dill as dill
import pandas as pd
from collections import defaultdict

# -------------------------------------------------------------Ted Talk------------------------------------------------#
eng_title_posting_list = defaultdict(lambda: defaultdict(list))
eng_document_posting_list = defaultdict(lambda: defaultdict(list))
eng_title_bigram_list = defaultdict(list)
eng_document_bigram_list = defaultdict(list)
eng_ids = []


# for t, d in zip(titles, descriptions):
#     print(t, "\n", d)


def create_positional_index():
    global eng_title_posting_list, eng_document_posting_list

    csv_data = pd.read_csv("./English_preproccess/ted_talks.csv")
    titles = csv_data['title']
    descriptions = csv_data['description']
    id = 0
    for title, description in zip(titles, descriptions):
        title_words = title.split(" ")
        description_words = description.split(" ")
        for i, t in enumerate(title_words):
            eng_title_posting_list[t][id].append(i)
        for i, d in enumerate(description_words):
            eng_document_posting_list[d][id].append(i)
        eng_ids.append(id)
        id += 1
    # print(eng_document_posting_list)
    return


def delete_positional_index(doc_id):
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


def add_positional_index(path):
    global eng_title_posting_list, eng_document_posting_list

    data = pd.read_csv(path)
    titles = data['title']
    descriptions = data['description']
    id = eng_ids[-1]
    eng_ids.append(id)
    for title, description in zip(titles, descriptions):
        # print(id, "    ", title, "  ", document)
        title_words = title.split(" ")
        description_words = description.split(" ")
        for i, t in enumerate(title_words):
            eng_title_posting_list[t][id].append(i)
        for i, d in enumerate(description_words):
            eng_document_posting_list[d][id].append(i)
    return


def get_positional_index(word, field):
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


def load_positional_index():
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


def save_positional_index():
    # title
    eng_title_positional = open("eng_title_positional.txt", "wb")
    dill.dump(eng_title_posting_list, eng_title_positional)
    eng_title_positional.close()
    # doc
    eng_doc_positional = open("eng_doc_positional.txt", "wb")
    dill.dump(eng_document_posting_list, eng_doc_positional)
    eng_doc_positional.close()
    return


def create_positional_bigram():
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


def delete_positional_bigram(word, field):
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


def add_positional_bigram(word, field):
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


def get_positional_bigram(bigram, field):
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


def save_positional_bigram():
    # title
    eng_title_bigram = open("eng_title_bigram.txt", "wb")
    dill.dump(eng_title_bigram_list, eng_title_bigram)
    eng_title_bigram.close()
    # doc
    eng_doc_bigram = open("eng_doc_bigram.txt", "wb")
    dill.dump(eng_document_bigram_list, eng_doc_bigram)
    eng_doc_bigram.close()
    return


def load_positional_bigram():
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


def wiki_create_index(path):
    global title_posting_list, document_posting_list
    data = pd.read_csv(path)
    titles = data['title']
    # todo change into text and id
    documents = data['description']
    id = data['comments']
    for doc_id, title, document in zip(id, titles, documents):
        # print(doc_id, "    ", title, "  ", document)
        title_words = title.split(" ")
        document_words = document.split(" ")
        for i, t in enumerate(title_words):
            title_posting_list[t][doc_id].append(i)
        for i, d in enumerate(document_words):
            document_posting_list[d][doc_id].append(i)
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
    # todo change into text and id
    documents = data['description']
    id = data['comments']
    for v in document_posting_list.values():
        if v.keys().__contains__(id):
            print("Document Already exists")
            return
    for doc_id, title, document in zip(id, titles, documents):
        print(doc_id, "    ", title, "  ", document)
        title_words = title.split(" ")
        document_words = document.split(" ")
        for i, t in enumerate(title_words):
            title_posting_list[t][doc_id].append(i)
        for i, d in enumerate(document_words):
            title_posting_list[d][doc_id].append(i)
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


create_positional_index()
create_positional_bigram()
save_positional_bigram()
save_positional_index()
## print(eng_title_posting_list)
## print(eng_document_posting_list)
## get_positional_index('salam', 'TITLE')
## delete_positional_index(0)
## get_positional_index('salam', 'TITLE')
## create_positional_bigram()
## print(eng_title_bigram_list)
## print(eng_document_bigram_list)
## get_positional_bigram('sa', 'TITLE')
## delete_positional_bigram('salam', 'TITLE')
## print(eng_title_bigram_list)
## print(eng_document_bigram_list)
## add_positional_bigram('al', 'TITLE')
## print(eng_title_bigram_list)

# create_positional_bigram()
# get_positional_bigram('sa', 'TEXT')
# wiki_create_index('ted_talks.csv')
# wiki_create_bigram()
# wiki_get_bigram('he', 'TEXT')
# wiki_get_index('help', 'TEXT')
# wiki_save_index()
# wiki_load_index()
# wiki_delete_index(101)
# wiki_get_index('help', 'TEXT')
# wiki_save_index("title.txt", "doc.txt")
# wiki_load_index("title.txt", "doc.txt")
# create_positional_index()
# get_positional_index('help', 'TEXT')
