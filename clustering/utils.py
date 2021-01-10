import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

from models.utils import tf_idf_ntn
from sklearn.decomposition import PCA
from preproccess_persian.persian_preproccess import preprocess

dir = "../datasets/phase3"

def json_to_csv(name):
    def has_vulnerable_values(df, which, criteria):
        strs = df[[which, criteria]].values.tolist()
        size = len(strs)
        neq = sum([preprocess(strs[i][0]) != preprocess(strs[i][1]) for i in range(size)])
        percent = neq / size
        return percent > 0.3

    f = os.path.join(dir, name)
    df = pd.read_json(f)
    # if not has_vulnerable_values(df, "link", "title"):
    #     df.drop("link", axis=1, inplace=True)
    new_name = name.replace("json", "csv")
    f = os.path.join(dir, new_name)
    df.to_csv(f, index=False)

def bag_of_words(X):
    vocab = set()
    for doc in X:
        tokens = doc.split()
        for t in tokens:
            vocab.add(t)

    return sorted(list(vocab))

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


def word2vec():
    #TODO complete here
    pass

def dim_reduction(type, X, from_scratch=False):
    if type == "PCA":
        if not from_scratch:
            k = 500
            pca = PCA(k)
            x_transformed = pca.fit_transform(X)
        else:
            thresh = 0.95
            cov = np.matmul(X.T, X)
            U, S, V = np.linalg.svd(cov)
            eig_vals = S.diagonal()
            percent = np.array([(eig_vals[i] / sum(eig_vals)) for i in range(len(eig_vals))])
            k = np.where(percent > thresh)[0]
            print(k, S.shape)
            print(U.shape)
            x_transformed = np.matmul(X, U[,:k])
            return x_transformed

    elif type == "TSNE":
        k = 500
        tsne = TSNE(k)
        x_transformed = tsne.fit_transform(X)
    else:
        raise Exception("Unknown dimension reduction type!!!")
    return x_transformed

# json_to_csv("hamshahri.json")
# preprocess_csv("hamshahri.csv")
