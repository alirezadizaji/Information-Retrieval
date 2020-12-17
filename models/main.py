import pandas as pd
import numpy as np

from NaiveBayes import NB
from KNN import KNN
from RFC import Random_Forest
from SVM import SVM
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
    elif type == "NaiveBayes":
        model = NB
    elif type == "SVM":
        model = SVM
    else:
        raise Exception("Unknown mode!!!")
    return model

def conv2vec(df, vocab, mode, y_label="views"):
    X, y = df.drop(y_label, axis=1).apply(' '.join, axis=1).to_numpy(), df[y_label].to_numpy()
    X = tf_idf_ntn(X, vocab)
    print(X.shape)
    # plot_tsne(X, y, "{} Dataset (separated features)".format(mode))
    return X, y


if __name__ == '__main__':
    type="SVM"
    train_df = pd.read_csv(train_path, index_col=0)
    test_df = pd.read_csv(test_path, index_col=0)
    vocab = bag_of_words()
    X_train, y_train = conv2vec(train_df, vocab, "Train")
    X_test, y_test = conv2vec(test_df, vocab, "Test")

    KF_idxs = create_KF_idxs(X_train, k=5)
    model = get_cfr(type)

    print("------------{}-----------".format(type))
    if type == "RFC":
        cfr = model(params= {"mode": "Train", "X": X_train, "y": y_train, "KF_idxs": KF_idxs})
        model(params= {"mode": "Test", "X": X_test, "y": y_test, "cfr": cfr})

    elif type == "KNN":
        K = [1, 5, 9]
        best_k = model(params={"mode": "Train", "X": X_train, "y": y_train, "KF_idxs": KF_idxs, "K": K})
        model(params={"mode": "Test", "X_train": X_train, "y_train": y_train,
                            "X_test": X_test, "y_test": y_test,"k": best_k})
    elif type == "NaiveBayes":
        prior, cond_prob, terms_to_number = model(params={"mode": "Train"})
        model(params={"mode": "Test", "prior": prior, "cond_prob": cond_prob, "terms_to_number": terms_to_number})

    elif type == "SVM":
        C = [0.5, 1, 1.5, 2]
        cfr, best_c = model(params={"mode": "Train", "X": X_train, "y": y_train, "C": C, "split": 0.2})
        model(params={"mode": "Test", "X": X_test, "y": y_test, "cfr": cfr, "C": best_c})
