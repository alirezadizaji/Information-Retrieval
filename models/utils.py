import math
import numpy as np
from sklearn.model_selection import KFold
from sklearn.manifold import TSNE
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import os


def plot_tsne(X, y, title):
  if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
    X = np.array(X)
    y = np.array(y)

  y = np.squeeze(y)
  size = X.shape[0]
  X = X.reshape(size, -1)
  print("------")
  print(X.shape, y.shape)
  print("------")
  # scaler = StandardScaler()
  # x = scaler.fit_transform(x)
  # print(scaler.mean_.shape, scaler.var_.shape)

  perp_range = [15]
  num_iter_range = [1000]
  for num_iter in num_iter_range:
    for perp in perp_range:
      model = TSNE(n_components=2, random_state=0, perplexity=perp, n_iter=num_iter)
      tsne_data = model.fit_transform(X)
      tsne_data = np.vstack((tsne_data.T, y)).T
      tsne_df = pd.DataFrame(data=tsne_data, columns=("Dim_1", "Dim_2", "label"))
      sn.FacetGrid(tsne_df, hue="label", size=6).map(plt.scatter, 'Dim_1', 'Dim_2').add_legend()
      plt.subplots_adjust(top=0.95)
      plt.title(title)
      dir = os.path.join("../plots", "{}_{}_{}.jpg".format(title, perp, num_iter))
      plt.savefig(dir)
      print("completed with perp: {}, n_iter: {}".format(perp, num_iter))


def smoothing(arr):
    return arr + 1

# calculate True/False Positive/Negative
def get_pos_negs(y_val, y_pred):
    tp = np.sum((y_val == 1) * (y_pred == 1), axis=0)
    tn = np.sum((y_val == -1) * (y_pred == -1), axis=0)
    fp = np.sum(y_pred == 1, axis=0) - tp
    fn = np.sum(y_pred == -1, axis=0) - tn
    return np.vstack((tp, fp, tn, fn)).squeeze()

def create_KF_idxs(X_train, k=5):
    KF = KFold(k, shuffle=True)
    KF_idxs = []

    for train_idx, val_idx in KF.split(X_train):
        KF_idxs.append((train_idx, val_idx))

    return KF_idxs

def check_multi_dim(arr):
    if len(arr.shape) < 2:
        arr = arr[:, np.newaxis]
    return arr

def analyze_report(report, cfr, mode="Train", params=None):
    def get_res(pos_negs):
        tp, fp, tn, fn = smoothing(pos_negs)

        pr_pos = tp / (tp + fp)
        rc_pos = tp / (tp + fn)

        pr_neg = tn / (tn + fn)
        rc_neg = tn / (tn + fp)

        acc = (tp + tn) / (tp + fp + tn + fn)
        f1_pos = 2 * pr_pos * rc_pos / (pr_pos + rc_pos)
        f1_neg = 2 * pr_neg * rc_neg / (pr_neg + rc_neg)

        res = (acc, f1_pos, pr_pos, rc_pos, f1_neg, pr_neg, rc_neg)
        return res

    if cfr == "KNN":
        K = params["K"]
        pos_negs = np.mean(report, axis=0) if len(report.shape) == 3 else report  # mean for KFold
        shape = pos_negs.shape
        pos_negs = pos_negs[:, np.newaxis] if len(shape) == 1 else pos_negs
        new_shape = pos_negs.shape

        best_k, best_res = -1, (0, 0, 0, 0, 0, 0, 0)
        for i, k in zip(range(new_shape[1]), K):
            res = get_res(pos_negs[:, i])
            new_acc = res[0]
            prev_acc = best_res[0]
            if new_acc >= prev_acc:
                best_k = k
                best_res = res
        print("{} Result -> best_k: {}, best_result(Acc, "
              "F1_pos, Pr_pos, Rc_pos, F1_neg, Pr_neg, Rc_neg): {}"
              .format(mode, best_k, best_res))

        if mode == "Test":
            pass
        else:
            return best_k

    elif cfr == "RFC":
        pos_negs = np.mean(report, axis=0) if len(report.shape) == 2 else report  # mean for KFold
        res = get_res(pos_negs)
        print("{} Result -> (Acc, "
              "F1_pos, Pr_pos, Rc_pos, F1_neg, Pr_neg, Rc_neg): {}"
              .format(mode, res))

def tf_idf_ntn(col, vocab):
    N = len(col)
    tf, df = {}, {}
    for i, doc in enumerate(col):
        tokens = doc.split()
        df_checked = []
        for t in tokens:
            tf.setdefault(t, {})
            tf[t].setdefault(i, 0)
            tf[t][i] += 1
            df.setdefault(t, 0)
            df[t] = df[t] + 1 if t not in df_checked else df[t]
            df_checked.append(t)

    idf = {k: math.log(N / v) for k,v in df.items()}
    tf_idf = np.zeros((N, len(vocab)))
    for i, doc in enumerate(col):
        tokens = doc.split()
        for t in tokens:
            j = vocab.index(t)
            tf_idf[i][j] = tf[t][i] * idf[t]
    return tf_idf

def bag_of_words(y_label="views"):
    root = "../datasets"
    phase1 = os.path.join(root, "phase1")
    phase2 = os.path.join(root, "phase2")
    phase1_file = os.path.join(phase1, "prepared_english.csv")
    phase2_files = [os.path.join(phase2, f) for f in ["prepared_test.csv", "prepared_train.csv"]]
    csv_files = [phase1_file]
    csv_files.extend(phase2_files)

    datasets = []
    for f in csv_files:
        df = pd.read_csv(f, index_col=0)
        if y_label in df.columns:
            df.drop(y_label, inplace=True, axis=1)
        doc_set = df.apply(' '.join, axis=1).to_numpy() #concat all columns
        datasets.append(doc_set)

    X = np.concatenate(datasets, axis=0).squeeze()
    vocab = set()
    for doc in X:
        tokens = doc.split()
        for t in tokens:
            vocab.add(t)

    return sorted(list(vocab))
