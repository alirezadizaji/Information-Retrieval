
import networkx as nx
import  json



def PageRank(filename , num_top , alpha):
    f = open(filename,)
    articles = json.load(f)
    G = nx.Graph()

    for a in articles:
        id = a["id"]
        G.add_node(id)
        for ref in a["references"]:
             G.add_edge(id,ref)

    ranks=nx.pagerank(G,alpha)
    print(ranks)
    high_ranked=sorted(ranks)[-num_top:]
    print("high_ranked",high_ranked)
