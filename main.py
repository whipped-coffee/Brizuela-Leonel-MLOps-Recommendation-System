import pandas as pd
from fastapi import FastAPI

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

@app.get('/movies_in_language/{language}')
def movies_in_language(language: str):
    data = pd.read_csv('_src/data/movies_normalized.csv', usecols=['release_language','id'])
    movie_counts = {f'count movies produced in {language}': data.loc[data['release_language'] == str(language), 'id'].count().item()}
    return movie_counts

@app.get('/movie_runtime/{movie}')
def movie_runtime(movie: str):
    data = pd.read_csv('_src/data/movies_normalized.csv', usecols=['title','runtime','release_year'])
    movie_data = {'movie': movie,
                  'runtime': data.loc[data['title'] == movie, 'runtime'].values[0].astype(int).item(),
                  'release_year': data.loc[data['title'] == movie, 'release_year'].values[0].item()}
    return movie_data

@app.get('/collection/{movie}')
def collection(movie: str):
    data = pd.read_csv('_src/data/movies_normalized.csv', usecols=['collection_name','id','revenue'])
    if (data.loc[data['collection_name'].str.contains(str(movie), regex=True)].shape[0] > 1):
        collection_data = {'collection': data.loc[data['collection_name'].str.contains(str(movie), regex=True), 'collection_name'].values[1],
                      'count_movies': data.loc[data['collection_name'].str.contains(str(movie), regex=True), 'id'].count().item(),
                      'total_revenue': data.loc[data['collection_name'].str.contains(str(movie), regex=True), 'revenue'].sum().item(),
                      'mean_revenue': data.loc[data['collection_name'].str.contains(str(movie), regex=True), 'revenue'].mean().item()}
        return collection_data    
    else: return ('The movie you selected its not part of a collection.')

@app.get('/movies_in_country/{country}')
def movies_per_country(country: str):
    data = pd.read_csv('_src/data/movies_normalized.csv', usecols=['prod_country','id'])
    country_data = {f'total of movies produced in {country}': data.loc[data['prod_country'] == str(country), 'id'].count().item()}
    return country_data

@app.get('/prod_company_success/{company}')
def prod_company_success(company: str):
    data = pd.read_csv('_src/data/movies_normalized.csv', usecols=['prod_companies','id','revenue'])
    data.loc[data['prod_companies'].isna(), 'prod_companies'] = 'None'
    company_data = {'company': company,
                  'total_movies': data.loc[data['prod_companies'].str.contains(str(company), regex=True), 'id'].count().item(),
                  'total_revenue': data.loc[data['prod_companies'].str.contains(str(company), regex=True), 'revenue'].sum().item()}
    return company_data

@app.get('/director_data/{director}')
def director_data(director: str):
    data = pd.read_csv('_src/data/movies_normalized.csv', usecols=['title', 'release_date', 'budget', 'revenue', 'return','director'])
    movies_data_list = []
    movies_data_list = [['title', 'release_date', 'budget', 'revenue', 'return']]
    for i in range(data.loc[data['director'] == str(director), 'title'].shape[0]):
        movies_data_list.append([])
        movies_data_list[i] = {'title': data.loc[data['director'] == str(director), 'title'].values[i],
                                 'release_date': data.loc[data['director'] == str(director), 'release_date'].values[i],
                                 'budget': str(data.loc[data['director'] == str(director), 'budget'].values[i]),
                                 'revenue': str(data.loc[data['director'] == str(director), 'revenue'].values[i]),
                                 'return': str(data.loc[data['director'] == str(director), 'return'].values[i])}
        director_data = {'director':str(director),
                         'total_movies_return': str(round(data.loc[data['director'] == str(director), 'return'].sum().item(),2)),
                         'produced_movies': movies_data_list}
    return(director_data)     

