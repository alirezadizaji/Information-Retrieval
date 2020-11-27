import numpy as np
from sklearn.model_selection import KFold
from scipy import stats as stat
#
X = np.zeros((10, 1500))
y = np.zeros((10))
y[500:] = 1
y[:500] = -1
kf = KFold(5)

kf_idxs = []
for train_idx, val_idx in kf.split(X):
    kf_idxs.append((train_idx, val_idx))



def dup_cols(arr, indx, num_dups=1):
    if len(arr.shape) < 2:
        arr = arr[:, np.newaxis]
    return np.insert(arr,[indx+1]*num_dups,arr[:,[indx]],axis=1)

def check_multi_dim(arr):
    if len(arr.shape) < 2:
        arr = arr[:, np.newaxis]
    return arr


def smoothing(arr):
    return arr + 1

#get best k and validation results
def analyze_report(report, K, mode="Train"):
        unit_res = np.mean(report, axis=0) if len(report.shape) == 3 else report #mean for KFold
        shape = unit_res.shape
        best_k, best_res = -1, (0, 0, 0, 0, 0, 0, 0)
        for i, k in zip(range(shape[1]), K):
            tp, fp, tn, fn = smoothing(unit_res[:, i])

            pr_pos = tp / (tp + fp)
            rc_pos = tp / (tp + fn)

            pr_neg = tn / (tn + fn)
            rc_neg = tn / (tn + fp)

            acc = (tp + tn) / (tp + fp + tn + fn)
            f1_pos = 2 * pr_pos * rc_pos / (pr_pos + rc_pos)
            f1_neg = 2 * pr_neg * rc_neg / (pr_neg + rc_neg)

            if acc >= best_res[0]:
                best_k = k
                best_res = (acc, f1_pos, pr_pos, rc_pos, f1_neg, pr_neg, rc_neg)
        print("{} Result -> best_k: {}, best_result(Acc, "
              "F1_pos, Pr_pos, Rc_pos, F1_neg, Pr_neg, Rc_neg): {}"
              .format(mode, best_k, best_res))

        if mode == "Test":
            pass
        else:
            return best_k


# calculate True/False Positive/Negative
def get_primary_result(y_val, y_pred):
    tp = np.sum((y_val == 1) * (y_pred == 1), axis=0)
    tn = np.sum((y_val == -1) * (y_pred == -1), axis=0)
    fp = np.sum(y_pred == 1, axis=0) - tp
    fn = np.sum(y_pred == -1, axis=0) - tn
    return np.vstack((tp, fp, tn, fn))

def KNN(X, y, kf_idxs, K, mode="Train"):
    if mode == "Train":
        assert isinstance(kf_idxs, (list, np.ndarray)) and isinstance(K, (list, np.ndarray))
        shape = (len(kf_idxs), 4, len(K))  # 4 = tp, fp, tn, fn
        report = np.zeros(shape)

        for i, (t_idx, v_idx) in enumerate(kf_idxs):
            X_train, y_train = X[t_idx], y[t_idx]
            X_val, y_val = X[v_idx], y[v_idx]
            y_val = check_multi_dim(y_val)
            row = y_val.shape[0]
            y_pred = np.zeros((row, len(K)))

            for j, x in enumerate(X_val):
                dist = np.linalg.norm(x - X_train)
                for l, k in enumerate(K):
                    nearest = dist.argsort()[-k:][::-1]
                    y_nearest = y_train[nearest]
                    y_pred[j, l] = stat.mode(y_nearest)[0]

            report[i] = get_primary_result(y_val, y_pred)
        return analyze_report(report, K, mode)

    elif mode == "Test":
        assert isinstance(kf_idxs, int) and isinstance(K, int)
        train_idx = kf_idxs

        X_train, y_train = X[:train_idx], y[:train_idx]
        X_test, y_test = X[train_idx:], y[train_idx:]
        y_pred = np.empty_like(y_test)
        for i, x in enumerate(X_test):
            dist = np.linalg.norm(x - X_train)
            nearest = dist.argsort()[-K:][::-1]
            y_nearest = y_train[nearest]
            y_pred[i] = stat.mode(y_nearest)[0]

        report = get_primary_result(y_test, y_pred)
        analyze_report(report, K=[K], mode=mode)

    else:
        print("Unknown mode!!!")

KNN(X, y, kf_idxs, mode="Train", K=[1, 5, 9])