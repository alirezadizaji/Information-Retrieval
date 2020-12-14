from Classifier.KNN import KNN
from Classifier.RFC import Random_Forest
from Classifier.utils import create_KF_idxs
from English_preproccess import preproccess

train_path = "train.csv"
test_path = "test.csv"
preproccess.PreProccess_for_classifier(train_path, test_path)

def get_cfr(type):
    model = None
    if type == "RFC":
        model = Random_Forest
    elif type == "KNN":
        model = KNN
    else:
        raise Exception("Unknown mode!!!")
    return model

kf_idxs = create_KF_idxs(X, k=5)

type="RFC"

model = get_cfr(type)

model()

