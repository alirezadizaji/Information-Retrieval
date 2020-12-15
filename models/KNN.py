import numpy as np
from sklearn.model_selection import KFold
from scipy import stats as stat
from utils import *

def KNN(params):
    mode = params["mode"]

    if mode == "Train":
        keys = ["KF_idxs", "K", "X", "y"]
        KF_idxs, K, X, y = (params[k] for k in keys)
        report = np.zeros((len(KF_idxs), 4, len(K))) # 4 = tp, fp, tn, fn

        for i, (t_idx, v_idx) in enumerate(KF_idxs):
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

            report[i] = get_pos_negs(y_val, y_pred)
        best_k = analyze_report(report, "KNN", mode, params={"K": K})
        return best_k

    elif mode == "Test":
        keys = ["k", "X_train", "y_train", "X_test", "y_test"]
        k, X_train, y_train, X_test, y_test = (params[k] for k in keys)
        y_pred = np.empty_like(y_test)

        for i, x in enumerate(X_test):
            dist = np.linalg.norm(x - X_train)
            nearest = dist.argsort()[-k:][::-1]
            y_nearest = y_train[nearest]
            y_pred[i] = stat.mode(y_nearest)[0]

        report = get_pos_negs(y_test, y_pred)
        analyze_report(report, "KNN", mode, params={"K": [k]})

    else:
        print("Unknown mode!!!")