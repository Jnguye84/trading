from sklearn import decomposition
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
#citation:
#https://www.youtube.com/watch?v=oiusrJ0btwA&pp=ygUScGNhIGRhdGEgcHJvZmVzc29y
X = df.iloc[:,:].values

#elbow method
wcss = []
for i in range(1,11):
    k_means = KMeans(n_clusters=i,init='k-means++', random_state=42)
    k_means.fit(X)
    wcss.append(k_means.inertia_)
#plot elbow curve
plt.plot(np.arange(1,11),wcss)
plt.xlabel('Clusters')
plt.ylabel('SSE')
plt.show()

num = #this is the number from where the elbow is

k_means_optimum = KMeans(n_clusters = num, init = 'k-means++',  random_state=42)
y = k_means_optimum.fit_predict(X)
print(y)

df['cluster'] = y  
df1 = df[df.cluster==0]
df2 = df[df.cluster==1]

kplot = plt.axes(projection='3d')
xline = np.linspace(0, 15, 1000)
yline = np.linspace(0, 15, 1000)
zline = np.linspace(0, 15, 1000)
kplot.plot3D(xline, yline, zline, 'black')

# Data for three-dimensional scattered points
kplot.scatter3D(df1.Positive, df1.Neutral, df1.Negative, c='red', label = 'Cluster 1')
kplot.scatter3D(df2.Positive,df2.Neutral,df2.Negative, c ='green', label = 'Cluster 2')
plt.scatter(k_means_optimum.cluster_centers_[:,0], k_means_optimum.cluster_centers_[:,1], color = 'indigo', s = 200)
plt.legend()
plt.title("Kmeans")
plt.show()

score = silhouette_score(X,y)
print(score)
