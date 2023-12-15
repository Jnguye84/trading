from sklearn import decomposition
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
#from sa_on_news import df, df_list_of_sources
import kmeans
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('data.csv')
df = df[['Positive','Neutral','Negative','URL']]
lst = []
X = df[['Positive', 'Negative']]

def KCluster(num, X, df):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(X)
    k_means_optimum = KMeans(n_clusters = num)
    y = k_means_optimum.fit_predict(scaled_features)
    cluster_centers = k_means_optimum.cluster_centers_

    # Find the most important cluster
    cluster_sizes = np.unique(y, return_counts=True)[1]
    most_important_cluster = np.argmax(cluster_sizes)

    df['cluster'] = y  
    df1 = df[df.cluster==0]
    df2 = df[df.cluster==1]
    df3 = df[df.cluster == 2]
    df4 = df[df.cluster == 3]

    # Calculate the Silhouette score
    s = silhouette_score(X, y)

    return s, df1, df2, df3, df4, most_important_cluster, cluster_centers

for num in range (2,10):
    lst.append(KCluster(num, X, df)[0]) #lst of silhouette scores

idx = lst.index(max(lst)) #finding number of optimal clusters

#plot
s, df1, df2, df3, df4, most_important_cluster, cluster_centers = KCluster(idx, X, df)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(df1['Positive'] , df1['Negative'])
ax.scatter(df2['Positive'] , df2['Negative'])
ax.scatter(df3['Positive'] , df3['Negative'])
ax.scatter(df4['Positive'] , df4['Negative'])

u_labels = np.unique(df.cluster)

print('The value of the center of this cluster is    ' '[Positive, Negative]')
print('                                          ', cluster_centers[most_important_cluster])

j = np.argmax(abs(cluster_centers[most_important_cluster]))
if j == 0:
    print('Sentiment from Finbert is classified as Positive')
else:
    print('General sentiment from Finbert is classified as Negative')

for i in u_labels:
    ax.scatter(df[df['cluster'] == i]['Positive'] , df[df['cluster'] == i]['Negative'] , label = i)

# Set labels
ax.set_xlabel('Positive')
ax.set_ylabel('Negative')

# Add legend
ax.legend()

plt.show()

