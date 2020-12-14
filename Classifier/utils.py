import math

import numpy as np
from sklearn.model_selection import KFold


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
        K = params["k"]
        pos_negs = np.mean(report, axis=0) if len(report.shape) == 3 else report  # mean for KFold
        shape = pos_negs.shape
        best_k, best_res = -1, (0, 0, 0, 0, 0, 0, 0)
        for i, k in zip(range(shape[1]), K):
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

def tf_idf_ntn(col):
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
    words = sorted(list(df.keys()))
    tf_idf = np.zeros((N, len(words)))
    for i, doc in enumerate(col):
        tokens = doc.split()
        for t in tokens:
            j = words.index(t)
            tf_idf[i][j] = tf[t][i] * idf[t]
    return tf_idf
