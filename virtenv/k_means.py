from sklearn import decomposition
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sa_on_news import df, df_list_of_sources
#citation:
#https://www.youtube.com/watch?v=oiusrJ0btwA&pp=ygUScGNhIGRhdGEgcHJvZmVzc29y

X = df.iloc[:,:].values
num = 4

k_means_optimum = KMeans(n_clusters = num, init = 'k-means++',  random_state=42)
y = k_means_optimum.fit_predict(X)
print(y)

df['cluster'] = y  
df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster == 2]
df4 = df[df.cluster == 3]

kplot = plt.axes(projection='3d')
xline = np.linspace(0, 1, 1000)
yline = np.linspace(0, 1, 1000)
zline = np.linspace(0, 1, 1000)
kplot.plot3D(xline, yline, zline, 'black')

# Data for three-dimensional scattered points
kplot.scatter3D(df1.Positive, df1.Neutral, df1.Negative, c='red', label = 'Cluster 1')
kplot.scatter3D(df2.Positive,df2.Neutral,df2.Negative, c ='green', label = 'Cluster 2')
kplot.scatter3D(df3.Positive,df3.Neutral,df3.Negative, c ='blue', label = 'Cluster 3')
kplot.scatter3D(df4.Positive,df4.Neutral,df4.Negative, c ='pink', label = 'Cluster 4')
plt.scatter(k_means_optimum.cluster_centers_[:,0], k_means_optimum.cluster_centers_[:,1], color = 'indigo', s = 200, label=df_list_of_sources)
plt.legend()
plt.title("Kmeans")
plt.show()

score = silhouette_score(X,y)
print(score)

# Get the clusters and categories distributions
cluster_distrib = df['Cluster'].value_counts()

# Plot both
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(16,6))
axs[1].set_title("Cluster Distribution", fontsize='x-large', y=1.02)

sns.barplot(x=cluster_distrib.index, y=cluster_distrib.values, ax=axs[1], color='b')


