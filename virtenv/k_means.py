from sklearn import decomposition
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
#from sa_on_news import df, df_list_of_sources
import kmeans
import warnings

from sa_on_news import main

ticker = input('ticker:')
name = input('name:')

warnings.filterwarnings("ignore")
lst = []

df = main(ticker, name)

X = df[['Positive', 'Negative']]

k_means_optimum = KMeans(n_clusters = 4)
y = k_means_optimum.fit_predict(X[['Positive', 'Negative']])
cluster_centers_ = k_means_optimum.cluster_centers_

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

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(df1['Positive'] , df1['Negative'])
ax.scatter(df2['Positive'] , df2['Negative'])
ax.scatter(df3['Positive'] , df3['Negative'])
ax.scatter(df4['Positive'] , df4['Negative'])

u_labels = np.unique(df.cluster)

print('The value of the center of this cluster is    ' '[Positive, Negative]')
print('                                          ', cluster_centers_[most_important_cluster])

j = np.argmax(abs(cluster_centers_[most_important_cluster]))
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

