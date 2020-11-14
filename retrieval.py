from collections import defaultdict
import math
import numpy as np


# import English_preproccess.preproccess as ep
# import Presian_preproccess.preproccess as pp

# DOC_TYPE = 'Eng'


# ret_text_posting_list = defaultdict(lambda: defaultdict(list))
# ret_title_posting_list = defaultdict(lambda: defaultdict(list))
# tot_documents = 0


def calc_tf(tf):
    if tf == 0:
        return 1
    else:
        return 1 + math.log(tf, 10)


def calc_idf(df, tot_documents):
    return math.log((tot_documents / (df + 1)), 10)


def create_title_tf_table(ret_title_posting_list, title_term_to_number, tot_documents, title_terms):
    # global ret_title_posting_list, title_terms, title_term_to_number
    # title_terms = list(ret_title_posting_list.keys())
    # title_term_to_number = {t: i for i, t in enumerate(title_terms)}
    tf = np.zeros((tot_documents, len(title_terms)))
    for t in ret_title_posting_list.keys():
        for d in ret_title_posting_list[t].keys():
            tf[d][title_term_to_number[t]] = calc_tf(len(ret_title_posting_list[t][d]))

    return tf


def create_text_tf_table(ret_text_posting_list, text_term_to_number, tot_documents, text_terms):
    # global ret_text_posting_list, text_terms, text_term_to_number
    # text_terms = list(ret_text_posting_list.keys())
    # text_term_to_number = {t: i for i, t in enumerate(text_terms)}
    tf = np.zeros((tot_documents, len(text_terms)))
    for t in ret_text_posting_list.keys():
        for d in ret_text_posting_list[t].keys():
            tf[d][text_term_to_number[t]] = calc_tf(len(ret_text_posting_list[t][d]))
    return tf


def create_title_idf(title_terms, title_term_to_number, ret_title_posting_list, tot_documents):
    idf = [0] * len(title_terms)
    for t in ret_title_posting_list.keys():
        idf[title_term_to_number[t]] = calc_idf(len(ret_title_posting_list[t]), tot_documents)
    return idf


def create_text_idf(text_terms, text_term_to_number, ret_text_posting_list, tot_documents):
    idf = [0] * len(text_terms)
    for t in ret_text_posting_list.keys():
        idf[text_term_to_number[t]] = calc_idf(len(ret_text_posting_list[t]), tot_documents)
    return idf


def calc_title_weights(title_tf, title_idf):
    # global title_tf, title_idf
    for d in range(title_tf.shape[0]):
        w = 0
        for t in range(title_tf.shape[1]):
            title_tf[d][t] = title_tf[d][t] * title_idf[t]
            w += title_tf[d][t] ** 2


        w = math.sqrt(w)
        for t in range(title_tf.shape[1]):
            if w == 0:
                w=1
            title_tf[d][t] = title_tf[d][t] / w

    return title_tf


def calc_text_weights(text_tf, text_idf):
    # global text_tf, text_idf
    for d in range(text_tf.shape[0]):
        w = 0
        for t in range(text_tf.shape[1]):
            text_tf[d][t] = text_tf[d][t] * text_idf[t]
            w += text_tf[d][t] ** 2
        w = math.sqrt(w)
        for t in range(text_tf.shape[1]):
            if w == 0:
                w=1
            text_tf[d][t] = text_tf[d][t] / w

    return text_tf


def ltc_lnc(header, query, title_weights, text_weights, title_term_to_number, text_term_to_number,
            ret_title_posting_list, ret_text_posting_list, tot_documents):
    # global title_weights, text_weights
    # if DOC_TYPE == 'Eng':
    #     query = ep.clean_text(query)
    # else:
    #     query = pp.prepare_text(query)
    query_terms = query.split()
    print(query_terms)
    if header == 'title':
        query_terms_ = [q for q in query_terms if q in ret_title_posting_list.keys()]
        query_ = {i: calc_tf(query_terms_.count(i)) for i in np.unique(query_terms_)}
        print(query_)
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


# def retrieve_posting_lists():
#     global ret_text_posting_list, ret_title_posting_list, tot_documents, indexing
#     if DOC_TYPE == 'Eng':
#         indexing.eng_create_index()
#         ret_text_posting_list = indexing.eng_document_posting_list
#         ret_title_posting_list = indexing.eng_title_posting_list
#         tot_documents = indexing.eng_total_documents
#     else:
#         indexing.wiki_create_index()
#         ret_text_posting_list = indexing.document_posting_list
#         ret_title_posting_list = indexing.title_posting_list
#         tot_documents = indexing.wiki_total_documents


def add_scores(title_scores, text_scores):
    id_score_pair = list(enumerate(np.add(title_scores, text_scores)))
    max_ = max(10, len(id_score_pair))
    s = sorted(id_score_pair, key=lambda x: x[1], reverse=True)[:max_]
    return s


def search(query, ret_title_posting_list, ret_text_posting_list, tot_documents):
    title_terms = list(ret_title_posting_list.keys())
    title_term_to_number = {t: i for i, t in enumerate(title_terms)}
    text_terms = list(ret_text_posting_list.keys())

    text_term_to_number = {t: i for i, t in enumerate(text_terms)}
    title_tf = create_title_tf_table(ret_title_posting_list, title_term_to_number, tot_documents, title_terms)
    text_tf = create_text_tf_table(ret_text_posting_list, text_term_to_number, tot_documents, text_terms)
    title_idf = create_title_idf(title_terms, title_term_to_number, ret_title_posting_list, tot_documents)
    text_idf = create_text_idf(text_terms, text_term_to_number, ret_text_posting_list, tot_documents)
    title_weights = calc_title_weights(title_tf, title_idf)
    text_weights = calc_text_weights(text_tf, text_idf)
    title_scores = ltc_lnc('title', query, title_weights, text_weights, title_term_to_number, text_term_to_number,
                           ret_title_posting_list, ret_text_posting_list, tot_documents)

    text_scores = ltc_lnc('text', query, title_weights, text_weights, title_term_to_number, text_term_to_number,
                          ret_title_posting_list, ret_text_posting_list, tot_documents)
    best_doc_ids = add_scores(title_scores, text_scores)
    print(best_doc_ids)
