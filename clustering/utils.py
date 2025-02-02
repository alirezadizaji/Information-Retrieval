import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from gensim.models import Word2Vec, Doc2Vec

from classifying.utils import tf_idf_ntn
from sklearn.decomposition import PCA
from preproccess_persian.persian_preproccess import preprocess

dir = "../datasets/phase3"


def json_to_csv(name):
    f = os.path.join(dir, name)
    df = pd.read_json(f)
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


def word_2_vec(x):
    sentences = [list(x[i].split(" ")) for i in range(len(x))]
    model = Word2Vec(sentences, min_count=2, size=50, iter=200)
    N = len(x)
    word_2_vec = np.zeros((N, 50))
    i = 0
    for s in sentences:
        tot = 0
        for w in s:
            if w in model.wv:
                tot += model.wv[w]
        word_2_vec[i] = (tot / len(s))
        i += 1
    return word_2_vec


def dim_reduction(type, X, k=100):
    if X.shape[1] <= k:
        return X
    if type == "PCA":
        pca = PCA(k)
        x_transformed = pca.fit_transform(X)
    elif type == "TSNE":
        tsne = TSNE(k)
        x_transformed = tsne.fit_transform(X)
    else:
        raise Exception("Unknown dimension reduction type!!!")
    return x_transformed


def plot(X, labels, alg, type, truth=False, dim=2):
    if dim > 3:
        raise Exception("plot dim should be 2 or 3!!!")
    x_trans = dim_reduction("PCA", X, dim)
    if dim == 2:
        _, ax = plt.subplots()
        ax.scatter(x_trans[:, 0], x_trans[:, 1], c=labels, s=50, cmap='viridis')
    else:
        ax = plt.axes(projection='3d')
        ax.scatter3D(x_trans[:, 0], x_trans[:, 1], x_trans[:, 2], c=labels, s=50, cmap='viridis')
        ax.set_zlabel("x3")
    which = "truth" if truth else "pred"
    ax.set_title("clustering to {} {} groups".format(len(set(labels)), which))
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    pth = "./plot/{}_{}_{}.png".format(alg, type, which).lower()
    plt.savefig(pth)
    plt.show()

# json_to_csv("hamshahri.json")
# preprocess_csv("hamshahri.csv")
