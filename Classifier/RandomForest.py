import numpy as np
from sklearn.model_selection import KFold
from scipy import stats as stat
from sklearn.ensemble import RandomForestClassifier

kf = KFold(5)

kf_idxs = []
for train_idx, val_idx in kf.split(X):
    kf_idxs.append((train_idx, val_idx))

# calculate True/False Positive/Negative
def get_primary_result(y_val, y_pred):
    tp = np.sum((y_val == 1) * (y_pred == 1), axis=0)
    tn = np.sum((y_val == -1) * (y_pred == -1), axis=0)
    fp = np.sum(y_pred == 1, axis=0) - tp
    fn = np.sum(y_pred == -1, axis=0) - tn
    return np.vstack((tp, fp, tn, fn))

#get validation results
def analyze_report(report):
        unit_res = np.mean(report, axis=0) if len(report.shape) == 2 else report #mean for KFold
        tp, fp, tn, fn = smoothing(unit_res[:, i])

        pr_pos = tp / (tp + fp)
        rc_pos = tp / (tp + fn)

        pr_neg = tn / (tn + fn)
        rc_neg = tn / (tn + fp)

        acc = (tp + tn) / (tp + fp + tn + fn)
        f1_pos = 2 * pr_pos * rc_pos / (pr_pos + rc_pos)
        f1_neg = 2 * pr_neg * rc_neg / (pr_neg + rc_neg)

        res = (acc, f1_pos, pr_pos, rc_pos, f1_neg, pr_neg, rc_neg)
        print("{} Result -> (Acc, "
              "F1_pos, Pr_pos, Rc_pos, F1_neg, Pr_neg, Rc_neg): {}"
              .format(mode, res))


def RFC(X, y, idxs, mode="Train", classfier=None):
    rf = RandomForestClassifier() if not classfier else classfier

    if mode == "Train":
        assert isinstance(idxs, (list, np.ndarray))
        shape = (len(idxs), 4) # 4 = tp, fp, tn, fn
        report = np.zeros(shape)
        for i, (t_idx, v_idx) in enumerate(idxs):
            X_train, y_train = X[t_idx], y[t_idx]
            X_val, y_val = X[v_idx], y[v_idx]

            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_val)

            report[i] = get_primary_result(y_val, y_pred)
        analyze_report(report)
        return rf

    if mode == "Test":
        assert isinstance(idxs, (int))
        train_idx = idxs
        X_test, y_test = X[train_idx:], y[train_idx:]
        y_pred = rf.predict(X_test)
        report = get_primary_result(y_test, y_pred)
        analyze_report(report)

    else:
        print("Unknown mode!!!")

rfc = RFC(X, y, kf_idxs)
# RFC(X, y, mode="Test", idxs=50000, classfier=rfc)

