import numpy as np
from sklearn.model_selection import KFold
from scipy import stats as stat
from sklearn.ensemble import RandomForestClassifier
from Classifier.utils import *

def Random_Forest(X, y, idxs, mode="Train", classfier=None):
    rfc = RandomForestClassifier() if not classfier else classfier

    if mode == "Train":
        assert isinstance(idxs, (list, np.ndarray))
        shape = (len(idxs), 4) # 4 = tp, fp, tn, fn
        report = np.zeros(shape)
        for i, (t_idx, v_idx) in enumerate(idxs):
            X_train, y_train = X[t_idx], y[t_idx]
            X_val, y_val = X[v_idx], y[v_idx]

            rfc.fit(X_train, y_train)
            y_pred = rfc.predict(X_val)

            report[i] = get_pos_negs(y_val, y_pred)
        analyze_report(report, "RFC", mode)
        return rfc

    if mode == "Test":
        assert isinstance(idxs, (int))
        train_idx = idxs
        X_test, y_test = X[train_idx:], y[train_idx:]
        y_pred = rfc.predict(X_test)
        report = get_pos_negs(y_test, y_pred)
        analyze_report(report, "RFC", mode)

    else:
        print("Unknown mode!!!")
