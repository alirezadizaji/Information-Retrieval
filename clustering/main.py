from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from clustering.utils import *

def get_data(file_name, type, features, label):
    f = os.path.join(dir, file_name)
    df = pd.read_csv(f, usecols=[*features, label])
    X = df[features].apply(' '.join, axis=1).to_numpy().squeeze()
    y = df[label].astype('category').cat.codes.to_numpy()
    vocabs = bag_of_words(X)
    if type == "tf_idf":
        X = tf_idf_ntn(X, vocabs)
    elif type == "word2vec":
        #TODO complete word2vec func in clustering.utils
        pass
    else:
        raise Exception("Unknown type!!!")

    return X, y

def algorithm(type, num_labels):
    if type == "GMM":
        model =GaussianMixture(num_labels)
    elif type == "KMeans":
        #TODO: complete here
        pass
    elif type == "Hierarchical":
        #TODO: complete here
        pass
    else:
        print("Unknown type!!!")

    return model
csv_name = "hamshahri.csv"
X, y_true = get_data(csv_name, "tf_idf", features=["summary", "title"], label="tags")
num_labels = np.unique(y_true).shape[0]
model = algorithm("GMM", num_labels)
X = dim_reduction("PCA", X, from_scratch=True)
y_pred = model.fit_predict(X)
print(adjusted_rand_score(y_true, y_pred))
print(normalized_mutual_info_score(y_true, y_pred))