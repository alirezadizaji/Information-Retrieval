from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from clustering.utils import *
from sklearn.cluster import AgglomerativeClustering, KMeans
from crawling.rank import PageRank


def get_data(file_name, type, features, label):
    f = os.path.join(dir, file_name)
    df = pd.read_csv(f)
    links = df['link']
    x = df[features].apply(' '.join, axis=1).to_numpy().squeeze()
    y = df[label].astype('category').cat.codes.to_numpy()

    vocabs = bag_of_words(x)
    if type == "tf_idf":
        x = tf_idf_ntn(x, vocabs)
    elif type == "word2vec":
        x = word_2_vec(x)
    else:
        raise Exception("Unknown type!!!")

    return x, links, y


def save(labels, links, path):
    labels = pd.Series(labels, dtype=str)
    df = pd.concat([links, labels], axis=1)
    df.columns = ['link', 'y_pred']
    df.to_csv(path, index=False)


def algorithm(type, num_labels):
    if type == "GMM":
        model = GaussianMixture(num_labels)
    elif type == "KMeans":
        model = KMeans(n_clusters=num_labels, random_state=0)
    elif type == "Hierarchical":
        model = AgglomerativeClustering(n_clusters=num_labels, affinity='euclidean', linkage='ward')
        pass
    else:
        print("Unknown type!!!")

    return model


if __name__ == '__main__':

    print(" Choose a number:\n",
          "0- Clustring\n",
          "1- Crawling\n",
          "2- PageRank\n",
          "3- Quit")
    cmd = input()
    if cmd == '0':
        alg = input("Choose a Algorithm(Kmeans ,GMM ,Hierarchical): ")
        type = input("Choose preprocess type(tf_idf, word2vec): ")
        csv_name = "hamshahri.csv"
        X, links, y_true = get_data(csv_name, type, features=["summary", "title"], label="tags")
        num_labels = np.unique(y_true).shape[0]
        model = algorithm(alg, num_labels)
        X = dim_reduction("PCA", X)
        y_pred = model.fit_predict(X)
        plot(X, y_pred, alg)
        plot(X, y_true, alg, True)
        pth = "./res/{}_{}.csv".format(alg, type).lower()
        save(y_pred, links, pth)
        print(adjusted_rand_score(y_true, y_pred))
        print(normalized_mutual_info_score(y_true, y_pred))
    if cmd == '1':
        """
        already crawled, just checkout crawling folder
        """
        pass
    if cmd == '2':
        print("Enter alpha:")
        alpha = float(input())
        PageRank('../crawling/articles.json', 10, alpha)
