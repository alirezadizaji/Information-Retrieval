from hazm import Normalizer, word_tokenize, Stemmer, WordTokenizer, stopwords_list ,Lemmatizer
import os
import re
import pandas as pd
import numpy as np
import category_encoders as ce
import matplotlib.pyplot as plt

dir = "../datasets/phase3"
stemmer = Stemmer()
lemmatizer = Lemmatizer()
normalizer = Normalizer()

def preprocess(text):
    punctuations = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`؟،{|}؛~"""
    text = text.lower()
    text = re.sub('\d+', '', text)
    text = text.translate(str.maketrans(punctuations, ' ' * len(punctuations)))
    text = ' '.join(re.sub(r'[^ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپوئژآؤ \n]', ' ', text).split())
    text = text.strip()
    normalized_text = normalizer.normalize(text)
    words = word_tokenize(normalized_text)
    words = [w for w in words if w != '.']
    words = [w for w in words if w not in stopwords_list()]
    words = [lemmatizer.lemmatize(w) for w in words]
    pre_text = ' '.join(words)
    return pre_text

def json_to_csv(name):
    def has_vulnerable_values(df, which, criteria):
        strs = df[[which, criteria]].values.tolist()
        size = len(strs)
        neq = sum([preprocess(strs[i][0]) != preprocess(strs[i][1]) for i in range(size)])
        percent = neq / size
        return percent > 0.3

    f = os.path.join(dir, name)
    df = pd.read_json(f)
    if not has_vulnerable_values(df, "link", "title"):
        df.drop("link", axis=1, inplace=True)
    new_name = name.replace("json", "csv")
    f = os.path.join(dir, new_name)
    df.to_csv(f, index=False)

def preprocess_csv(name):
    def cast_to(df, cols, type):
        df = df.astype({col: type for col in cols})
        return df

    def break_tags(x):
        tags = x['tags'][2:-2].split(" > ")
        x['main_tag'] = tags[0]
        x['sub_tag'] = tags[1]
        return x

    f = os.path.join(dir, name)
    df = pd.read_csv(f, header=0)
    df = df.apply(break_tags, axis=1)
    category_cols = ["tags", "main_tag", "sub_tag"]
    df = cast_to(df, category_cols, "category")
    pre_cols = ["title", "summary"]
    for col in pre_cols:
        df[col] = df[col].apply(preprocess)
    df.to_csv(f, index=False)

# json_to_csv("hamshahri.json")
# preprocess_csv("hamshahri.csv")
