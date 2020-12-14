import numpy as np
from sklearn.model_selection import KFold
from scipy import stats as stat
from sklearn.ensemble import RandomForestClassifier
from utils import *


def Random_Forest(params):
    keys = ["mode", "X", "y"]
    mode, X, y = (params[k] for k in keys)

    if mode == "Train":
        KF_idxs = params["KF_idxs"]
        rfc = RandomForestClassifier()
        report = np.zeros((len(KF_idxs), 4))  # 4 = tp, fp, tn, fn
        for i, (t_idx, v_idx) in enumerate(KF_idxs):
            X_train, y_train = X[t_idx], y[t_idx]
            X_val, y_val = X[v_idx], y[v_idx]

            rfc.fit(X_train, y_train)
            y_pred = rfc.predict(X_val)

            report[i] = get_pos_negs(y_val, y_pred)
        analyze_report(report, "RFC", mode)
        return rfc

    if mode == "Test":
        rfc = params["cfr"]
        X_test, y_test = X, y
        y_pred = rfc.predict(X_test)
        report = get_pos_negs(y_test, y_pred)
        analyze_report(report, "RFC", mode)

    else:
        print("Unknown mode!!!")
