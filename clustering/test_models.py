
from clustering.main import *
from clustering.utils import *
import matplotlib.pyplot as plt


def plot_res(alg ,type, x_trans , y_pred , parameter):

        fig, axs = plt.subplots(len(parameter[0]),int(len(parameter)/len(parameter[0])))
        fig.suptitle(alg+" ,"+ type)
        c=0
        for j in range(len(parameter[0])):
            for i in range(int(len(parameter)/len(parameter[0]))):
                axs[j, i].scatter(x_trans[:, 0], x_trans[:, 1], c=y_pred[c], s=20, cmap='viridis')
                axs[j, i].set_title(parameter[c])
                c=c+1
        plt.show()


gmm_params = [

            {
                'n_components': 20,
                'max_iter': 50,
                'random_state':None,
             },
            {
                'n_components': 40,
                'max_iter': 50,
                'random_state':None,
             },
            {
                'n_components': 60,
                'max_iter': 50,
                'random_state':None,
             },

    {
                'n_components': 50,
                'max_iter': 100,
                'random_state':None,
             },
            {
                'n_components': 50,
                'max_iter': 150,
                'random_state':None,
             },

    {
                'n_components': 50,
                'max_iter': 200,
                'random_state':None,
             },
]
km_params = [

            {
                'n_clusters':20,
                'max_iter': 50,
                'random_state':None,
             },
            {
                'n_clusters': 40,
                'max_iter': 50,
                'random_state':None,
             },
            {
                'n_clusters': 60,
                'max_iter': 50,
                'random_state':None,
             },

    {
                'n_clusters': 50,
                'max_iter': 100,
                'random_state':None,
             },
            {
                'n_clusters': 50,
                'max_iter': 150,
                'random_state':None,
             },

    {
                'n_clusters': 50,
                'max_iter': 200,
                'random_state':None,
             },
]
hierarical_params = [

            {
                'n_clusters':20,
                'linkage': 'average',
             },
            {
                'n_clusters': 40,
                'linkage': 'average',
             },
            {
                'n_clusters': 60,
                'linkage': 'average',
             },

    {
                'n_clusters': 80,
                'linkage': 'single',
             },
            {
                'n_clusters': 100,
                'linkage': 'single',
             },

    {
                'n_clusters': 120,
                'linkage': 'single',
             },
     {
                'n_clusters': 10,
                'linkage': 'single',
             },
]

def test(alg,type):
    csv_name = "hamshahri.csv"
    y_pred =[]
    X, links, y_true = get_data(csv_name, type, features=["summary", "title"], label="tags")
    X = dim_reduction("PCA", X)
    x_trans = dim_reduction("PCA", X, 2)

    if alg =='GMM':
        for param in gmm_params:
                gmm = GaussianMixture(**param)
                y_pred.append(gmm.fit_predict(X))
        plot_res(alg, type,x_trans,y_pred,gmm_params)


    if alg =='Kmeans':
        for param in km_params:
                kmean = KMeans(**param)
                y_pred.append(kmean.fit_predict(X))
        plot_res(alg, type  ,x_trans,y_pred,km_params)

    if alg =='Hierarchical':
        for param in hierarical_params:
                hirchal = AgglomerativeClustering(**param)
                y_pred.append(hirchal.fit_predict(X))
        plot_res(alg,type ,x_trans,y_pred,hierarical_params)

    for x in y_pred:
        print("ARI = ",adjusted_rand_score(y_true, x) , "normalize = ",normalized_mutual_info_score(y_true, x))

