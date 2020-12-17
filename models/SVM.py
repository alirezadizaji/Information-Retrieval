import numpy as np
import pandas as pd
from sklearn import svm, metrics
from sklearn.metrics import *
from models.utils import *
from sklearn.model_selection import cross_val_score , KFold

def SVM(params):

        C = params["C"]
        mode = params["mode"]
        keys = ["X_train" , "y_train" ,"X_test" ,"y_test"]
        X ,Y , X_test,y_test  = (params[k] for k in keys)

        for margin in C:

                clf = svm.SVC(kernel='rbf' ,gamma=0.001, C=margin)
                scores = []
                cv = KFold(n_splits=5)
                for train_idx, test_idx in cv.split(X):
                    X_tr, X_te, y_tr, y_te =X[train_idx], X[test_idx], Y[train_idx], Y[test_idx]
                    clf.fit(X_tr, y_tr)
                    scores.append(clf.score(X_te, y_te))


                if mode =="Train":
                    y_pred=clf.predict(X)
                    reprt = get_pos_negs(Y , y_pred)
                    print("C :",margin)
                    analyze_report(reprt , "SVM" , "Train" , params={"C":C})


                if mode =="Test":
                    y_pred=clf.predict(X_test)
                    reprt = get_pos_negs(y_test , y_pred)
                    print("C :",margin)
                    analyze_report(reprt , "SVM" , "Test" , params={"C":C})


