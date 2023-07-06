import pandas as pd
from fastapi import FastAPI
import re

app = FastAPI()

@app.get('/') # .get(server:port), '/' because its localhost
def index():
    text = {'introduction': "MLOps index's API create by Brizuela Leonel Ariel",
            'github': 'https://github.com/whipped-coffee',
            'gmail': 'leonelbrizuela159357@gmail.com',           
            'movies_in_language(language)':'Returns the count of movies made in that language',
            'movie_runtime(movie)':'Returns the runtime of the given movie',
            'collection(movie)':'Returns the collection name, total_revenue and mean_revenue of the given movie',
            'movies_in_country(country)':'Returns the count of movies made in that country',
            'prod_company_success(company)':'Returns company_name, total_movies made by that company, and the total_revenue',
            'director_data(director)':'returns the director_name, total_movies made by that director, the information of each movie'
            } 
    return text

@app.get('/peliculas_idioma/{language}')
def movies_in_language(language: str):
    try:
        data = pd.read_csv('_src/data/movies_transformed.csv', usecols=['original_language','id'])
        data.loc[data['original_language'].isna(), 'original_language'] = 'None'
        movie_counts = {f'movies count produced in {language}': len(data.loc[data['original_language'] == language, 'id'].unique())}
        
        return movie_counts
    except:
        return 'There is not any movie with that name'

@app.get('/peliculas_duracion/{movie}')
def movie_runtime(movie: str):
    data = pd.read_csv('_src/data/movies_transformed.csv', usecols=['title','runtime','release_year'])
    data.loc[data['title'].isna(), 'title'] = 'None'
    movie_data = []
    try:
        for i in range(data.loc[data['title'] == movie, 'title'].shape[0]):
            movie_data.append([])
            movie_data[i] = {'movie': data.loc[data['title'] == movie, 'title'].values[i],
                    'runtime': data.loc[data['title'] == movie, 'runtime'].values[i].astype(int).item(),
                    'release_year': data.loc[data['title'] == movie, 'release_year'].values[i].item()}
        return movie_data
    except:
        return 'There is not any movie with that name'

@app.get('/franquicia/{movie}')
def collection(movie: str):
    regex = re.compile(movie, re.IGNORECASE) # Make the condition case insensitive
    data = pd.read_csv('_src/data/movies_transformed.csv', usecols=['collection_name','id','revenue'])
    try:
        collection_data = {'collection': data.loc[data['collection_name'].str.contains(regex, regex=True), 'collection_name'].values[1],
                      'count_movies': data.loc[data['collection_name'].str.contains(regex, regex=True), 'id'].count().item(),
                      'total_gain': data.loc[data['collection_name'].str.contains(regex, regex=True), 'revenue'].sum().item(),
                      'mean_gain': data.loc[data['collection_name'].str.contains(regex, regex=True), 'revenue'].mean().item()}
        return collection_data
    except:
        return 'The inputed movie its not part of a collection.'

@app.get('/peliculas_pais/{country}')
def movies_per_country(country: str):
    data = pd.read_csv('_src/data/movies_transformed.csv', usecols=['prod_countries','id'])
    data.loc[data['prod_countries'].isna(), 'prod_countries'] = 'None'
    regex = re.compile(country, re.IGNORECASE)
    try:
        movie_counts = data.loc[data['prod_countries'].str.contains(regex, regex=True), 'id'].count().item() 
        country_data = {f'total of movies produced in {country}': movie_counts}
        return country_data
    except:
        return 'There is not any movie made in the inputed country'

@app.get('/productoras_exitosas/{company}')
def prod_company_success(company: str):
    regex = re.compile(company, re.IGNORECASE)
    data = pd.read_csv('_src/data/movies_transformed.csv', usecols=['prod_companies','id','revenue'])
    data.loc[data['prod_companies'].isna(), 'prod_companies'] = 'None'
    try:
        company_data = {'company': company,
                    'total_movies': data.loc[data['prod_companies'].str.contains(regex, regex=True), 'id'].count().item(),
                    'total_revenue': data.loc[data['prod_companies'].str.contains(regex, regex=True), 'revenue'].sum().item()}
        return company_data
    except:
        return {'There is no company with the name that you ingresed in the database'}

@app.get('/get_director/{director}')
def director_data(director: str):
    data = pd.read_csv('_src/data/movies_transformed.csv', usecols=['title', 'release_date', 'budget', 'revenue', 'return','directors'])
    data.loc[data['directors'].isna(), 'directors'] = 'None'
    regex = re.compile(director, re.IGNORECASE)
    try:
        movies_data_list = []
        movies_data_list = [['title', 'release_date', 'budget', 'revenue', 'return']]
        for i in range(data.loc[data['directors'].str.contains(regex, regex=True), 'title'].shape[0]):
            movies_data_list.append([])
            movies_data_list[i] = {'title': data.loc[data['directors'].str.contains(regex, regex=True), 'title'].values[i],
                                    'release_date': data.loc[data['directors'].str.contains(regex, regex=True), 'release_date'].values[i],
                                    'budget': str(data.loc[data['directors'].str.contains(regex, regex=True), 'budget'].values[i]),
                                    'revenue': str(data.loc[data['directors'].str.contains(regex, regex=True), 'revenue'].values[i]),
                                    'return': str(data.loc[data['directors'].str.contains(regex, regex=True), 'return'].values[i])}
            director_data = {'director':director,
                            'total_movies_return': str(round(data.loc[data['directors'].str.contains(regex, regex=True), 'return'].sum().item(),2)),
                            'produced_movies': movies_data_list}
        return director_data
    except:
        return 'There is no director with that name'  
 

