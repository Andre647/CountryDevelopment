import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
import pycountry_convert as pc
import plotly.express as px
import streamlit as st
import tempfile



warnings.filterwarnings("ignore")

def criar_grafico(coluna):
    plt.figure()  
    sns.histplot(x=coluna)

    fig = plt.gcf()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig.savefig(temp_file.name)

    plt.close(fig)
    return temp_file.name

def country_to_continent(CountryName):
    try:
        country_code = pc.country_name_to_country_alpha2(
            CountryName, cn_name_format="default"
        )
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)

        return continent_name

    except Exception:
        return np.nan

def country_to_isocode(country):
    try:
        return pycountry.countries.get(name=country).alpha_3
    except Exception:
        return np.nan
    
"# Data"

URL = "https://raw.githubusercontent.com/Andre647/CountryDevelopment/refs/heads/main/data/Country-data.csv"
df = pd.read_csv(URL)

if st.checkbox('Show dataframe'): 
    st.dataframe(df, use_container_width=True)
    df.shape
st.divider()

"## Data Understanding"


dic = pd.read_csv("https://raw.githubusercontent.com/Andre647/CountryDevelopment/refs/heads/main/data/data-dictionary.csv")
content = {}
for index, row in dic.iterrows():
    content[row['Column Name'].lower()] = row['Description']



left_column2, right_column2 = st.columns(2)
for palavra, texto in content.items():
    with st.expander(palavra):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(texto)
        with col2:
            st.image(criar_grafico(df[palavra]), use_column_width=True)

"""### Child Mortality"""

fig, ax = plt.subplots(1, 2, figsize=(10, 6), sharey=True)

sns.scatterplot(x='total_fer', y='child_mort', data=df, ax=ax[0])
ax[0].set_xlabel('Fertility Rate')
ax[0].set_ylabel('Child Mortality Rate')

sns.scatterplot(x='life_expec', y='child_mort', data=df, ax=ax[1])
ax[1].set_xlabel('Life Expectancy')

plt.subplots_adjust(wspace=0, hspace=0)
st.pyplot(fig)

"""### Income"""

fig, ax = plt.subplots(1, 2, figsize=(10, 6), sharey=True)

sns.scatterplot(x='total_fer', y='income', data=df, ax=ax[0])
ax[0].set_xlabel('Fertility Rate')
ax[0].set_ylabel('Income')

sns.scatterplot(x='life_expec', y='income', data=df, ax=ax[1])
ax[1].set_xlabel('Life Expectancy')

plt.subplots_adjust(wspace=0, hspace=0)
st.pyplot(fig)

"""We could create several different charts, what can be analyzed is that a country's **income** significantly affects important factors when considering it as developed, such as **life expectancy**. Another obvious factor we can observe is that the infant mortality rate increases along with the fertility rate, while life expectancy, in turn, decreases.

### Continents
"""

df['continent'] = df['country'].apply(country_to_continent)

fig, ax = plt.subplots(1, 1, figsize=(12, 6))

sns.barplot(
    x='continent', y='income',
    palette='Set2',
    ci=None,
    ax=ax,
    data=df
)

ax2 = ax.twinx()

sns.lineplot(
    x='continent', y='inflation',
    data=df, color='red',
    ax=ax2, marker='o',
    linestyle='--', ci=None
)

ax.set_title('Income and Inflation (mean) by Continent')
ax.set_xlabel('Continent')
ax.set_ylabel('Income')

st.pyplot(fig)

"""Analyzing the inflation and income of countries and continents, we can reach interesting conclusions:

* Europe leads in income flow and has the lowest inflation, while Asia, although closely behind, has considerable inflation, likely due to the high inflation rate in Mongolia, although China's is not that low either;

* Africa has an extremely low income flow combined with high inflation, only lower than that of South America, which certainly affects the continent's development and the cluster we will perform;

* Despite not having the highest median, South America has the highest average inflation.
"""
st.divider()
df['ISO_code'] = df['country'].apply(country_to_isocode)

plot_type = st.selectbox("Select plot", ['child_mort', 'exports', 'health',	'imports', 'income', 'inflation', 'life_expec', 'total_fer', 'gdpp'])
colors_palette = {
    'child_mort': px.colors.sequential.Jet,
    'exports': px.colors.sequential.Blues,
    'health':  px.colors.sequential.Blugrn,
    'imports': px.colors.sequential.Brwnyl,
    'income' : px.colors.sequential.Blugrn,
    'inflation' : px.colors.sequential.Redor,
    'life_expec' : px.colors.sequential.Blues,
    'total_fer' : px.colors.sequential.Burg,
    'gdpp' : px.colors.sequential.Blugrn
}

fig = px.choropleth(
    df,
    locations="ISO_code",
    color=plot_type,
    hover_data=["continent", "country", plot_type],
    height=500,
    color_continuous_scale=colors_palette[plot_type]
)

fig.update_layout(
    title={
        'text': '<b>Distribution of <b>' + plot_type.capitalize() +  '<b> on the World Map</b>',
        'font': {'size': 20, 'color': 'black'}
    }
)

fig.update_xaxes(tickfont_family="Arial Black")
st.plotly_chart(fig, use_container_width=True)




