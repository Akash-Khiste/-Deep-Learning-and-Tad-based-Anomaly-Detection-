import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix
from sklearn import datasets
from sklearn.decomposition import PCA
from TADClassifier import tad_classify
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('Taddata.csv')
scaler = StandardScaler()
res = tad_classify(scaler.fit_transform(df.values))

print(df.head())

plot = True
if plot:
    df['anomaly']=0
    outliers_flat = res['scores'].keys()
    df.anomaly.ix[outliers_flat] = 1
    scatter_matrix(df.ix[:,:4], c=df.anomaly, s=(25 + 50*df.anomaly), alpha=.8)
    plt.show()

    print('Anomalies:', res['outliers'])
    g = res['g']
    X_pca = PCA().fit_transform(df)
    pos = dict((i,(X_pca[i,0], X_pca[i,1])) for i in range(X_pca.shape[0]))
    colors = []
    labels = {}
    for node in g.nodes():
        if node in outliers_flat:
            labels[node] = node
            colors.append('r')
        else:
            labels[node] = ''
            colors.append('b')
    nx.draw(g, pos=pos, node_color = colors)
    nx.draw_networkx_labels(g,pos,labels)
    plt.show()
