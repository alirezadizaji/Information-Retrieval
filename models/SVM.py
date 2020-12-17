from copy import deepcopy

import numpy as np
import pandas as pd
from sklearn import svm, metrics
from sklearn.metrics import *
from utils import *
from sklearn.model_selection import cross_val_score, KFold, train_test_split


def SVM(params):
    keys = ["mode", "C", "X", "y"]
    mode, C, X, y = (params[k] for k in keys)

    if mode == "Train":
        split = params["split"]
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split, shuffle=True)
        best_cfr, best_acc, best_c = None, 0, 0
        for margin in C:
             clf = svm.SVC(kernel='rbf' ,gamma=0.001, C=margin)
             clf.fit(X_train, y_train)
             y_pred = clf.predict(X_val)
             report = get_pos_negs(y_val, y_pred)
             acc = analyze_report(report , "SVM" , mode, params={"C": margin})

             if acc > best_acc:
                best_acc = acc
                best_cfr = deepcopy(clf)
                best_c = margin

        return best_cfr, best_c

    if mode == "Test":
        rfc = params["cfr"]
        X_test, y_test = X, y
        y_pred = rfc.predict(X_test)
        report = get_pos_negs(y_test, y_pred)
        analyze_report(report, "SVM", mode, params={"C": C})

    else:
        print("Unknown mode!!!")