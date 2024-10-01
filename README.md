# Country Developement Clustering

This project uses machine learning techniques to categorize a country based on his  socio-economics and health factors. 

## Table of Contents
- [Introduction](#introduction)
- [Data](#data)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Model Training](#model-training)
- [Results](#results)
- [Conclusion](#conclusion)

## Introduction
In this project, a clustering analysis of each country's development will be conducted. In this fictional scenario, HELP International has been able to raise around $10 million. Now, the CEO of the NGO needs to decide how to use this money strategically and effectively. Therefore, the CEO must make a decision to select the countries that are in the most urgent need of aid.


## Data
The dataset used in this project was cleaned and transformed to fit the model. You can explore the original data by downloading it from the following link:

- [Country Data](https://www.kaggle.com/datasets/rohan0301/unsupervised-learning-on-country-data)

### Exploratory Data Analysis (EDA)

This section provides insights into the dataset with visualizations and statistical summaries.

1. **Dataframe Display:**
   - Users can toggle the full dataset view.
   
2. **Visualization Options:**
   - **Child Mortality:** Shows how child mortality impacts life expectancy and fertility rate.
   - **Income:** Shows how Income affects life expectancy and fertility rate.
   - **Continent's Economy:** Visualizes the individual income and the inflation of each continent.
   - **World Map**: Using plotly, the user can see how each column is distribuited in the world.

3. **Insights:**
  - Europe leads in income flow and has the lowest inflation, while Asia, although closely behind, has considerable inflation, likely due to the high inflation rate in Mongolia, although China's is not that low either.

 - Africa has an extremely low income flow combined with high inflation, only lower than that of South America, which certainly affects the continent's development and the cluster we will perform.

 - Despite not having the highest median, South America has the highest average inflation.

## Model Training
The dataset was normalized, than the number of proper clusters was discovered and then an Agglomerative Model was conducted.

Steps:
1. Data was normalized.
2. The number of clusters were discovered with the elbow method.
3. The Agglomerative Cluster model from scikit-learn was used to fit.

## Results
![image](https://github.com/user-attachments/assets/13b225b2-1a35-456b-971b-1ebafea3a78b)

* [Project Video(PT-BR)](https://youtu.be/wKpKfJYoIjY)

## Conclusion
 - We can visualize that the countries in need of the most help are located on the African continent, specifically those centralized and near the Sahara Desert.
- The algorithm placed several Asian countries in the same cluster as countries from South America, as well as Eastern Europe.
- Haiti and Afghanistan are the only countries in extreme need that do not share a border with another country in the same cluster.
- Income and infant mortality are strong indicators of a country's development.
- 4 clusters was not ideal for the problem
  
(The data was collected in 2020 and does not reflect the current economic situation as of the time this notebook was created (2024).)

### [See for yourself](https://coutryclustering.streamlit.app/)
