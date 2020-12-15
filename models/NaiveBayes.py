import pandas as pd
import numpy as np
from English_preproccess import preproccess
from Indexing import eng_create_index


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


def naive_bayes():
    # todo use train data from prepared csv
    title_posting_list, document_posting_list, total_documents = eng_create_index(
        "C:/Users/Sabrineh Mokhtari/Desktop/darC/Term-7/MIR/Project/p2/project_phase2/Implementation/data.csv")

    df = pd.read_csv(
        "C:/Users/Sabrineh Mokhtari/Desktop/darC/Term-7/MIR/Project/p2/project_phase2/Implementation/data.csv")
    df = pd.DataFrame(df)
    train_labels = df['views'].replace(-1, 0)
    train_title_terms = df['title']
    train_text_terms = df['description']

    # todo use test data from prepared csv
    test_df = pd.read_csv(
        "C:/Users/Sabrineh Mokhtari/Desktop/darC/Term-7/MIR/Project/p2/project_phase2/Implementation/data.csv")
    test_df = pd.DataFrame(test_df)
    test_title_terms = test_df['title']
    test_text_terms = test_df['description']

    title_terms = list(title_posting_list.keys())
    title_term_to_number = {t: i for i, t in enumerate(title_terms)}

    text_terms = list(document_posting_list.keys())
    text_term_to_number = {t: i for i, t in enumerate(text_terms)}

    prior = prior_prob(train_labels)
    title_cond_prob = word_prob(title_term_to_number, train_title_terms, train_labels)
    text_cond_prob = word_prob(text_term_to_number, train_text_terms, train_labels)

    title_predictions = []
    text_predictions = []
    for title_q, text_q in zip(test_title_terms, test_text_terms):
        title_predict = predict_label(title_q, title_cond_prob, prior, title_term_to_number)
        title_predictions.append(title_predict)
        text_predict = predict_label(text_q, text_cond_prob, prior, text_term_to_number)
        text_predictions.append(text_predict)

    print("prior_probabilities:", prior)
    print("title_condition_probabilities:", title_cond_prob)
    print("text_condition_probabilities:", text_cond_prob)
    print("title_predictions:", title_predictions)
    print("text_predictions:", text_predictions)


naive_bayes()
