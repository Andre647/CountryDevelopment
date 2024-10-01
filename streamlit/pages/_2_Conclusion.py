import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry_convert as pc
import plotly.express as px
import streamlit as st


from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from pages._1_Visualization import df


mdata = df.drop(columns=['country', 'ISO_code', 'continent'])

"""## Normalization"""

scaler = StandardScaler()
scaler.fit(mdata)

mdata_scaled = scaler.transform(mdata)
mdata = pd.DataFrame(mdata_scaled, columns=mdata.columns)

if st.checkbox('Show data normalized'): 
    st.dataframe(mdata, use_container_width=True)
    mdata.shape
st.divider()

"### Dendogram"


fig = plt.figure(figsize=(10, 7))
Z = linkage(mdata, method='ward')
dendrogram(Z)

plt.xlabel('Countries')
plt.ylabel('Distance')

st.pyplot(fig)

"""### Elbow Method"""

inertia = []
K = range(1, 11)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(mdata)
    inertia.append(kmeans.inertia_)

fig = plt.figure(figsize=(8, 6))
plt.plot(K, inertia, 'bo-', markersize=8)
plt.xlabel('Clusters')
plt.ylabel('Inertia (Sum of Squared Distances)')
plt.title('Elbow Method')
st.pyplot(fig)

"The dendrogram provides us with an ideal number of **3 clusters**, while the elbow method seems to indicate that both 3 and 4 could work. We will perform both and check the results."
st.divider()
"## Agglomerative Clustering"

"The agglomerative model is less sensitive to outliers than K-Means. Since we are not concerned about performance here, it is a more robust model to use."

agg_clust = AgglomerativeClustering(
    n_clusters=3,
    linkage='ward'
)
st.write(agg_clust)
df['Cluster(3)'] = agg_clust.fit_predict(mdata)

"## Results"
df1 = df.copy()
df1['Cluster(3)'].loc[df1['Cluster(3)'] == 0] = 'No Help Needed'
df1['Cluster(3)'].loc[df1['Cluster(3)'] == 2] = 'Help Needed'
df1['Cluster(3)'].loc[df1['Cluster(3)'] == 1] = 'Might Need Help'

fig = px.choropleth(
    df1,
    locations="ISO_code",
    color='Cluster(3)',
    hover_data=["continent", "country", 'Cluster(3)'],
    height=500,
    color_discrete_map = {'Help Needed':'Red',
                          'No Help Needed':'Green',
                           'Might Need Help':'Yellow'}
                   )


fig.update_layout(
    title={
        'text': '<b>Clusters in the World Map</b>',
        'font': {'size': 20, 'color': 'black'}
    }
)
fig.update_geos(fitbounds = "locations", visible = True)
fig.update_xaxes(tickfont_family="Arial Black")
st.plotly_chart(fig, use_container_width=True)

st.divider()

fig, ax = plt.subplots(1, 2, figsize=(12, 6), sharex=True)

sns.boxplot(x='Cluster(3)', y='income', color='Green',data=df1, ax=ax[0])
ax[0].set_ylabel('Income')
ax[0].set_xlabel('')
ax[0].set_title('Income')

sns.boxplot(x='Cluster(3)', y='child_mort', color='Red',data=df1, ax=ax[1])
ax[1].set_ylabel('Child Mortality')
ax[1].set_xlabel('')
ax[1].set_title('Child Mortality')
st.pyplot(fig)

"""# Conclusion

* We can visualize that the countries in need of the most help are located on the African continent, specifically those centralized and near the Sahara Desert.
* The algorithm placed several Asian countries in the same cluster as countries from South America, as well as Eastern Europe.
* Haiti and Afghanistan are the only countries in extreme need that do not share a border with another country in the same cluster.
* Income and infant mortality are strong indicators of a country's development.
* 4 clusters was not ideal for the problem

(The data was collected in 2020 and does not reflect the current economic situation as of the time this notebook was created (2024).)
"""