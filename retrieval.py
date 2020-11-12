import math
from collections import defaultdict
import English_preproccess.preproccess as ep
import Presian_preproccess.preproccess as pp
import numpy as np
import Indexing

DOC_TYPE = 'Eng'
text_posting_list = defaultdict(lambda: defaultdict(list))
title_posting_list = defaultdict(lambda: defaultdict(list))
title_terms = list(title_posting_list.keys())
title_term_to_number = {t: i for i, t in enumerate(title_terms)}
text_terms = list(text_posting_list.keys())
text_term_to_number = {t: i for i, t in enumerate(text_terms)}
tot_documents = 0


def calc_length(l):
    tot = 0
    for i in range(len(l)):
        tot += l[i] ** 2
    return math.sqrt(tot)


def calc_tf(tf):
    if tf == 0:
        return 0
    else:
        return 1 + math.log(tf, 10)


def calc_idf(df):
    return math.log((tot_documents / (df + 1)), 10)


def create_title_tf_table():
    global title_posting_list, title_terms, title_term_to_number
    # title_terms = list(title_posting_list.keys())
    # title_term_to_number = {t: i for i, t in enumerate(title_terms)}
    tf = np.zeros((tot_documents, len(title_terms)), dtype=np.int)
    for t in title_posting_list.keys():
        for d in title_posting_list[t].keys():
            tf[d][title_term_to_number[t]] = calc_tf(len(title_posting_list[t][d]))
    return tf


def create_text_tf_table():
    global text_posting_list, text_terms, text_term_to_number
    # text_terms = list(text_posting_list.keys())
    # text_term_to_number = {t: i for i, t in enumerate(text_terms)}
    tf = np.zeros((tot_documents, len(text_terms)), dtype=np.int)
    for t in text_posting_list.keys():
        for d in text_posting_list[t].keys():
            tf[d][text_term_to_number[t]] = calc_tf(len(text_posting_list[t][d]))
    return tf


def create_title_idf():
    idf = [0] * len(title_terms)
    for t in title_posting_list.keys():
        idf[title_term_to_number[t]] = calc_idf(len(title_posting_list[t]))
    return idf


def create_text_idf():
    idf = [0] * len(text_terms)
    for t in text_posting_list.keys():
        idf[text_term_to_number[t]] = calc_idf(len(text_posting_list[t]))
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
        query = [q for q in query_terms if q in title_posting_list.keys()]
        query_ = {i: calc_tf(query.count(i)) for i in np.unique(query)}
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
        query = [q for q in query_terms if q in text_posting_list.keys()]
        query_ = {i: calc_tf(query.count(i)) for i in np.unique(query)}
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
    global text_posting_list, title_posting_list, tot_documents
    if DOC_TYPE == 'Eng':
        text_posting_list = Indexing.eng_document_posting_list
        title_posting_list = Indexing.eng_title_posting_list
        tot_documents = Indexing.eng_total_documents
    else:
        text_posting_list = Indexing.document_posting_list
        title_posting_list = Indexing.title_posting_list
        tot_documents = Indexing.wiki_total_documents


retrieve_posting_lists()
title_tf = create_title_tf_table()
text_tf = create_text_tf_table()
title_idf = create_title_idf()
text_idf = create_text_idf()
title_weights = calc_title_weights()
text_weights = calc_text_weights()


def add_scores(title_scores, text_scores):
    s = sorted(np.add(title_scores, text_scores))[:10]
    return s


def search(query):
    title_scores = ltc_lnc('title', "salam salam")
    text_scores = ltc_lnc('text', "salam salam")
    best_doc_ids = add_scores(title_scores, text_scores)


search("salam salam khubi")
