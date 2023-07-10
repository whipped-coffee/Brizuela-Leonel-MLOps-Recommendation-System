<h1 align='center'>
   MLOps Recommendation System Model
</h1>


<div style="display: flex; justify-content: center; align-items: center; height: 300px;">
  <img src="_src/assets/movies-img.jpg" alt="imagen de películas" width="400">
</div>

<h2 align = 'center'> Introduction </h2>

<p align = 'center'>
In this project, I assume the role of a Data Scientist working for a start-up that provides aggregation systems for streaming platforms. My responsibility is to oversee the entire process, from data gathering to the development and training of a content-based recommendation system model.
</p>    

## Objectives:

1. **Development of APIs that process functions and respond to data queries related to movies.**

2. **Development of a content-based recommendation system model**

<h2 align='center'> Summarize of the processes </h2>

## Extract, Transform & Load: [ETL.ipynb](https://github.com/whipped-coffee/Brizuela-Leonel-MLOps-Recommendation-System/blob/main/ETL.ipynb)
### In this file is the entire process of extracting, transformating and loading of the data obtained from the datasets. With the goal of preparing it for its future consumption. Such as mergin DataFrames, Unnesting data and Creation of aggregated columns

## Exploratory Data Analysis: [EDA.ipynb](https://github.com/whipped-coffee/Brizuela-Leonel-MLOps-Recommendation-System/blob/main/EDA.ipynb) 
### In this file is the entire process of the Exploratory Data Analysis with its respective documentation. This include: Handling the missing values, correlation matrix visualization and plotting of the distribution between the important features

## APIs functions: [main.py](https://github.com/whipped-coffee/Brizuela-Leonel-MLOps-Recommendation-System/blob/main/main.py)
### In this file we have the creation of a FastAPI system that can be consumed by the Data Analysis department, or a final user. It contains:
+ ### movies_in_language(language: str): It takes a language and returns the count of movies produced in that language
+ ### movie_runtime(movie: str): It takes a movie and returns its runtime and release_year
+ ### collection(franchise: str): It takes a franchise and returnss the movies_count, total_revenue and mean_revenue
+ ### movies_per_country(country: str): It takes a country and returns the count of movies produced in that country
+ ### prod_company_success(company: str): It takes a company and returns the total_revenue and the count of movies produced by that company
+ ### director_data(director: str): It takes a director's name and returns the success of the same measured by the tota_return. And it has to also returns the name of each movie with its release_date, individual_return, budget and revenue
+ ### recommendation(title: str): It takes a title of a movie and returns 5 recommendations for that movie


<div style="display:flex; align-items:center;">
  <div style="width:50%; padding-right:20px;">
    <h2>Used skills</h2>
    <ul style="text-align: justify;">
      <li><b> Scikit Learn</b>: Used for vectorize, tokenize & calculate the cosine similarity.</li>
      <li><b>Python</b>: Principal programming languages used in the Data Science field.</li>
      <li><b>Pandas</b>: Framework used to manage DataFrames.</li>
      <li><b>Matplotlib</b>: Framework used to plot data visualizations.</li>
      <li><b>FastAPI</b>: Framework used to create the users interface</li>
      <li><b>Uvicorn</b>: ASGI Server used to communicate with FastAPI.</li>
      <li><b>Render</b>: Deploy platform to upload the finished project.</li>
    </ul>
  </div>
</div>

## Considerations:
+ peliculas_duracion and recomendacion are case sensitive
+ recomendacion does not have all the movies because I had to reduce it to make the deploy

## Made by:
### Name: Brizuela Leonel Ariel
### GitHub: https://github.com/whipped-coffee
### Linkedin: https://www.linkedin.com/in/leonel-brizuela-30b80524a/
### Gmail: leonelbrizuela159357@gmail.com
