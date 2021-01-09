import pandas as pd
import numpy as np
from sklearn import metrics

from preprocess_english import preproccess
from Indexing import eng_create_index
from models.utils import *


def prior_prob(train_labels):
    n = len(train_labels)
    return [np.sum(train_labels == label) / n for label in range(2)]


def word_prob(term_to_number, train_terms, train_labels):
    word_count = [[0] * 2 for _ in range(len(term_to_number))]
    for terms, label in zip(train_terms, train_labels):
        term = terms.split(" ")
        for t in term:
            word_count[term_to_number[t]][label] += 1
    # print("word_count:", word_count)
    total_terms = [0] * 2
    for t in word_count:
        for i, c in enumerate(t):
            total_terms[i] += c
    # print("total_terms:", total_terms)
    B = len(term_to_number)
    return [[(w[i] + 1) / (total_terms[i] + B) for i in range(2)] for w in word_count]


def predict_label(query, cond_prob, prior, term_to_number):
    query = preproccess.prepare_text(query)
    query_terms = query.split(" ")
    probs = [np.log(p) for p in prior]
    for c in range(2):
        for q in query_terms:
            if q in term_to_number.keys():
                probs[c] += np.log(cond_prob[term_to_number[q]][c])
    # print("probs:", probs)
    label = -1 if np.argmax(probs) == 0 else 1
    return label


def NB(params):
    mode = params["mode"]
    if mode == "Train":
        title_posting_list, document_posting_list, total_documents = eng_create_index(
            "C:/Users/Sabrineh Mokhtari/Desktop/darC/Term-7/MIR/Project/p2/project_phase2/Implementation/datasets/phase2/prepared_train.csv")
        train_df = pd.read_csv(
            "C:/Users/Sabrineh Mokhtari/Desktop/darC/Term-7/MIR/Project/p2/project_phase2/Implementation/datasets/phase2/prepared_train.csv")
        train_df = pd.DataFrame(train_df)
        train_labels = train_df['views'].replace(-1, 0)
        train_title_terms = train_df['title']
        train_text_terms = train_df['description']
        train_terms = train_title_terms + " " + train_text_terms

        title_terms = list(title_posting_list.keys())
        text_terms = list(document_posting_list.keys())
        terms = set(title_terms + text_terms)
        terms_to_number = {t: i for i, t in enumerate(terms)}

        prior = prior_prob(train_labels)
        cond_prob = word_prob(terms_to_number, train_terms, train_labels)

        return prior, cond_prob, terms_to_number

    elif mode == "Test":
        cond_prob = params["cond_prob"]
        prior = params["prior"]
        terms_to_number = params["terms_to_number"]

        test_df = pd.read_csv(
            "C:/Users/Sabrineh Mokhtari/Desktop/darC/Term-7/MIR/Project/p2/project_phase2/Implementation/datasets/phase2/prepared_test.csv")
        test_df = pd.DataFrame(test_df)
        test_labels = test_df['views']
        test_title_terms = test_df['title']
        test_text_terms = test_df['description']
        test_terms = test_title_terms + " " + test_text_terms

        predictions = []
        for q in test_terms:
            predictions.append(predict_label(q, cond_prob, prior, terms_to_number))

        report = get_pos_negs(np.array(list(test_labels)), np.array(predictions))
        analyze_report(report, "NaiveBayes", "Test")


