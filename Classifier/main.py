import pandas as pd
import numpy as np
from KNN import KNN
from RFC import Random_Forest
from utils import *
# from English_preproccess import preproccess
# preproccess.PreProccess_for_classifier(train_path, test_path)

train_path = "prepared_train.csv"
test_path = "prepared_test.csv"

def get_cfr(type):
    model = None
    if type == "RFC":
        model = Random_Forest
    elif type == "KNN":
        model = KNN
    else:
        raise Exception("Unknown mode!!!")
    return model

def get_unique_words(train_df, test_df, y_label="views"):
    vocab = set()
    X_train = train_df.drop(y_label, axis=1).to_numpy()
    X_test = test_df.drop(y_label, axis=1).to_numpy()
    X = np.concatenate((X_train, X_test), axis=0)
    for collection in X.T:
        for doc in collection:
            token = doc.split()
            for t in token:
                vocab.add(t)
    vocab = sorted(list(vocab))
    print(len(vocab))
    return vocab
        
def convert_to_num(df, vocab, y_label="views"):
    X, y = df.drop(y_label, axis=1).apply(' '.join, axis=1).to_numpy(), df[y_label].to_numpy()
    X = tf_idf_ntn(X, vocab)
    print(X.shape, y.shape)
    return X, y

if __name__ == '__main__':
    type="RFC"
    train_df = pd.read_csv(train_path, index_col=0)
    test_df = pd.read_csv(test_path, index_col=0)
    vocab = get_unique_words(train_df,test_df)
    X_train, y_train = convert_to_num(train_df, vocab)
    X_test, y_test = convert_to_num(test_df, vocab)
    KF_idxs = create_KF_idxs(X_train, k=5)
    model = get_cfr(type)
    cfr = model(params= {"mode": "Train", "X": X_train, "y": y_train, "KF_idxs": KF_idxs})
    cfr = model(params= {"mode": "Test", "X": X_test, "y": y_test, "cfr": cfr})

