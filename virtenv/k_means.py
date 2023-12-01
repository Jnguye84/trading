from sklearn import decomposition
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sa_on_news import df, df_list_of_sources
import kmeans

X = df[['Positive', 'Negative', 'URL']]
num = 4

k_means_optimum = KMeans(n_clusters = num)
y = k_means_optimum.fit_predict(X)

df['cluster'] = y  
df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster == 2]
df4 = df[df.cluster == 3]

plt.scatter(df1[:,0] , df1[:,1])
plt.scatter(df2[:,0] , df2[:,1])
plt.scatter(df3[:,0] , df3[:,1])
plt.scatter(df4[:,0] , df4[:,1])
u_labels = np.unique(df.cluster)
centroids = kmeans.cluster_centers_
 
#plotting the results:
 
for i in u_labels:
    plt.scatter(df[df.cluster == i , 0] , df[df.cluster == i , 1] , label = i)
plt.scatter(centroids[:,0] , centroids[:,1] , s = 80, color = 'k')
plt.legend()
plt.show()