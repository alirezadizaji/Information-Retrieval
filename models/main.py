import pandas as pd
import numpy as np
from KNN import KNN
from RFC import Random_Forest
from utils import *
# from English_preproccess import preproccess
# preproccess.PreProccess_for_classifier(train_path, test_path)

train_path = "../datasets/phase2/prepared_train.csv"
test_path = "../datasets/phase2/prepared_test.csv"

def get_cfr(type):
    model = None
    if type == "RFC":
        model = Random_Forest
    elif type == "KNN":
        model = KNN
    else:
        raise Exception("Unknown mode!!!")
    return model

def conv2vec(df, vocabs, mode, y_label="views"):
    X, y = df.drop(y_label, axis=1).to_numpy(), df[y_label].to_numpy()
    cols = list(vocabs.keys())
    X = np.concatenate([tf_idf_ntn(doc, vocabs[c]) for c, doc in zip(cols, X.T)], axis=1)
    print(X.shape)
    # plot_tsne(X, y, "{} Dataset (separated features)".format(mode))
    return X, y

if __name__ == '__main__':
    type="RFC"
    train_df = pd.read_csv(train_path, index_col=0)
    test_df = pd.read_csv(test_path, index_col=0)
    vocabs = unique_words()
    X_train, y_train = conv2vec(train_df, vocabs, "Train")
    X_test, y_test = conv2vec(test_df, vocabs, "Test")
    KF_idxs = create_KF_idxs(X_train, k=5)
    model = get_cfr(type)
    cfr = model(params= {"mode": "Train", "X": X_train, "y": y_train, "KF_idxs": KF_idxs})
    cfr = model(params= {"mode": "Test", "X": X_test, "y": y_test, "cfr": cfr})

