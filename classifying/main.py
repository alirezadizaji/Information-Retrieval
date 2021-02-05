import pandas as pd
import numpy as np

from classifying.NaiveBayes import NB
from classifying.KNN import KNN
from classifying.RFC import Random_Forest
from classifying.SVM import *
from classifying.utils import *

from preprocess_english import preproccess
from Indexing import *
from proximity_search import *
from retrieval import search

train_path = "../datasets/phase2/prepared_train.csv" #datas
test_path = "../datasets/phase2/prepared_test.csv"
lbl_r = '1'
lbl_n= '-1'
def get_cfr(type):
    model = None
    if type == "RFC":
        model = Random_Forest
    elif type == "KNN":
        model = KNN
    elif type == "NaiveBayes":
        model = NB
    elif type == "SVM":
        model = SVM
    else:
        raise Exception("Unknown mode!!!")
    return model





def conv2vec(df, vocab, mode, y_label="views"):
    X, y = df.drop(y_label, axis=1).apply(' '.join, axis=1).to_numpy(), df[y_label].to_numpy()
    X = tf_idf_ntn(X, vocab)
    # print(X.shape)
    return X, y



def classification(best_c,train_path ,test_path):

    print("Start Classification ...")
    train_df = pd.read_csv(train_path, index_col=0)
    test_df = pd.read_csv(test_path, index_col=0)
    vocab = bag_of_words()
    X_train, y_train = conv2vec(train_df, vocab, "Train")

    X_test = test_df.apply(' '.join, axis=1).to_numpy()
    X_test = tf_idf_ntn(X_test, vocab)

    y_pred= SVMClassifier(params= {"X_test":X_test,"X_train": X_train, "Y_train": y_train, "C": best_c, "split": 0.2})
    store(test_df , y_pred)
    print("Done Classification. ")



if __name__ == '__main__':

    print(" Choose a number:\n",
                  "0- Models\n",
                  "1- Data classification\n",
                  "2- Search\n",
                  "3- Proximity Search\n",
                  "4- Quit"  )
    while True:
        cmd = input()

        if cmd == '0':
                print("Enter classifier type:")
                # type="RFC"
                type = str(input())
                train_df = pd.read_csv(train_path, index_col=0)
                test_df = pd.read_csv(test_path, index_col=0)
                vocab = bag_of_words()
                X_train, y_train = conv2vec(train_df, vocab, "Train")
                X_test, y_test = conv2vec(test_df, vocab, "Test")

                KF_idxs = create_KF_idxs(X_train, k=5)
                model = get_cfr(type)

                print("------------{}-----------".format(type))
                if type == "RFC":
                    cfr = model(params= {"mode": "Train", "X": X_train, "y": y_train, "KF_idxs": KF_idxs})
                    model(params= {"mode": "Test", "X": X_test, "y": y_test, "cfr": cfr})

                elif type == "KNN":
                    K = [1, 5, 9]
                    best_k = model(params={"mode": "Train", "X": X_train, "y": y_train, "KF_idxs": KF_idxs, "K": K})
                    model(params={"mode": "Test", "X_train": X_train, "y_train": y_train,
                                        "X_test": X_test, "y_test": y_test,"k": best_k})
                elif type == "NaiveBayes":
                    prior, cond_prob, terms_to_number = model(params={"mode": "Train"})
                    model(params={"mode": "Test", "prior": prior, "cond_prob": cond_prob, "terms_to_number": terms_to_number})

                elif type == "SVM":
                    C = [0.5, 1, 1.5, 2]
                    cfr, best_c = model(params={"mode": "Train", "X": X_train, "y": y_train, "C": C, "split": 0.2})
                    model(params={"mode": "Test", "X": X_test, "y": y_test, "cfr": cfr, "C": best_c})

        elif cmd == '1':
             print("Enter relevant & nonrelevant labels:")
             lbl_r , lbl_n = input().split()
             classification(1 , train_path , "/Users/atena/PycharmProjects/Information-Retrieval-Project/datasets/phase1/prepared_english.csv")

        elif cmd == '2':

            print("Enter Query")
            query = input()
            query=preproccess.prepare_text(query)

            print("Choose category : {},{}".format(lbl_r , lbl_n))
            category = input()

            if category == lbl_r:
                eng_title_posting_list, eng_document_posting_list, eng_total_documents = eng_create_index("../datasets/phase2/relevants.csv")
                print(eng_title_posting_list, "\n", eng_document_posting_list)

                search(query, eng_title_posting_list, eng_document_posting_list, eng_total_documents)

            if category == lbl_n:
                eng_title_posting_list, eng_document_posting_list, eng_total_documents = eng_create_index("../datasets/phase2/non_relevants.csv")
                print(eng_title_posting_list, "\n", eng_document_posting_list)

                search(query, eng_title_posting_list, eng_document_posting_list, eng_total_documents)


        elif cmd == '3':
                print("Enter Query like : word1 /range word2")
                query = input()

                key1 , key2 , size = proccess_query(query)

                print("Choose category : {},{}".format(lbl_r , lbl_n))
                category = input()

                if category == lbl_r:
                    eng_title_posting_list, eng_document_posting_list, eng_total_documents = eng_create_index("../datasets/phase2/relevants.csv")
                    doc_id_founded = CalculateOccurences(key1,key2,size , "../datasets/phase2/relevants.csv")
                    print("founded from proximity search: ",doc_id_founded)
                    for i in range(eng_total_documents):
                        if i not in doc_id_founded:
                            eng_title_posting_list,eng_document_posting_lis,eng_total_documents= eng_delete_index(i,eng_title_posting_list ,eng_document_posting_list,eng_total_documents)
                    search(key1+' '+key2 , eng_title_posting_list,eng_document_posting_list, eng_total_documents)

                if category == lbl_n:
                     eng_title_posting_list, eng_document_posting_list, eng_total_documents = eng_create_index("/Users/atena/PycharmProjects/Information-Retrieval-Project/datasets/phase2/relevants.csv")
                     doc_id_founded = CalculateOccurences(key1,key2,size , "/Users/atena/PycharmProjects/Information-Retrieval-Project/datasets/phase2/non_relevants.csv")
                     print("founded from proximity search: ",doc_id_founded)
                     for i in range(eng_total_documents):
                        if i not in doc_id_founded:
                            eng_title_posting_list,eng_document_posting_lis,eng_total_documents= eng_delete_index(i,eng_title_posting_list ,eng_document_posting_list,eng_total_documents)
                     search(key1+' '+key2 , eng_title_posting_list,eng_document_posting_list, eng_total_documents)

        elif cmd == '4':
            break
