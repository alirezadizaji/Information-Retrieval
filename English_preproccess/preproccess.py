import re
import tokenize

import pandas as pd

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def extract_data():
    df = pd.read_csv('ted_talks.csv')
    return  df



def listToString(lst):
    string = []
    for x in lst:
        x = x.split(" ")
        st = ' '.join(map(str, x))
        string.append(st)
    return string


def clean_text(text):

    tokens =word_tokenize(text)

    tokens = [word for word in tokens if word.isalpha()]
    # Lower the tokens
    tokens = [word.lower() for word in tokens]
    # Remove stopword
    tokens = [word for word in tokens if not word in stopwords.words("english")]
    # Lemmatize
    lemma = nltk.WordNetLemmatizer()
    tokens = [lemma.lemmatize(word, pos = "v") for word in tokens]
    tokens = [lemma.lemmatize(word, pos = "n") for word in tokens]
    tokens = ' '.join(tokens)
    return tokens

def pre_proccess(lst):
    print("Start preproccessing ...")
    pre_title =[]
    for title in lst:
        pre_title.append(clean_text(title))

    print("Done preproccessing.")
    return pre_title


def most_freq_words(df):
    listToStr = ' '.join([str(elem) for elem in df["title"]+df["description"]])
    word_count = Counter(listToStr)
    print(word_count.most_common(10))

df = extract_data()
print("most commen tokens:")
most_freq_words(df)

d = {'title': pre_proccess(listToString(df["title"])), 'description':pre_proccess(listToString(df["description"]))}
df_ = pd.DataFrame(d)
df_.to_csv(r'prepared_english.csv')
