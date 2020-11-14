import re
import tokenize

import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter


remove_lst=[]

def extract_data():
    df = pd.read_csv('/Users/atena/PycharmProjects/Information-Retrieval-Project/English_preproccess/ted_talks.csv')
    return  df



def listToString(lst):
    string = []
    for x in lst:
        x = x.split(" ")
        st = ' '.join(map(str, x))
        string.append(st)
    return string


def prepare_text(text):

    tokens =word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha()]

    # Remove stopword
    # tokens = [word for word in tokens if not word in stopwords.words("english")]
    # Remove 30 most commen words
    tokens = [word for word in tokens if not word in remove_lst]

    # Lower the tokens
    tokens = [word.lower() for word in tokens]
    # Lemmatize
    lemma = nltk.WordNetLemmatizer()
    tokens = [lemma.lemmatize(word, pos = "v") for word in tokens]
    tokens = [lemma.lemmatize(word, pos = "n") for word in tokens]
    tokens = ' '.join(tokens)

    return tokens

def pre_proccess(lst):

    pre_lst =[]
    for title in lst:
        pre_lst.append(prepare_text(title))


    return pre_lst


def most_freq_words():

    df = extract_data()
    listToStr = ' '.join(map(str, df['title']+df['description']))
    listToStr = word_tokenize(listToStr)
    word_count = nltk.FreqDist(listToStr)
    s = word_count.most_common(30)
    for x in s :
        remove_lst.append(x[0])
    return word_count.most_common(30)




def PreProccess():
    df = extract_data()
    most_freq_words()
    print("Start preproccessing ...")
    d = {'title': pre_proccess(listToString(df["title"])), 'description':pre_proccess(listToString(df["description"]))}
    print("Done preproccessing.")
    for i in range(len(d['title'])):
        if len(d['title'][i]) == 0:
            d['title'][i] = "No description"

    df_ = pd.DataFrame(d)
    df_.to_csv(r'prepared_english.csv')

