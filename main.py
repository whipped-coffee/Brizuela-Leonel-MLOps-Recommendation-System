import pandas as pd
import joblib
import re
from fastapi import FastAPI


app = FastAPI()

#Load the movie_data
data = pd.read_csv('_src/data/movies_transformed.csv')
model_data = pd.read_csv('_src/data/model_data.csv')
reduced_data = model_data.head(6000)

# load the compressed cosine similarity matrix
cosine_sim = joblib.load('_src/data/cosine_sim.pkl')

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
            'director_data(director)':'returns the director_name, total_movies made by that director, and the information of each produced movie'
            } 
    return text

@app.get('/peliculas_idioma/{language}')
def movies_in_language(language: str):
    try:       
        data['original_language'].fillna('', inplace = True)
        movie_counts = {f'movies count produced in {language}': len(data.loc[data['original_language'] == language, 'id'].unique())}       
        return movie_counts
    except:
        return 'There is not any movie with that name'

@app.get('/peliculas_duracion/{movie}')
def movie_runtime(movie: str):
    data['title'].fillna('', inplace = True)
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

@app.get('/franquicia/{franchise}')
def collection(franchise: str):
    data['collection_name'].fillna('', inplace=True)
    regex = re.compile(franchise, re.IGNORECASE) # Make the condition case insensitive
    try:
        franchise_data = {'collection': data.loc[data['collection_name'].str.contains(regex, regex=True), 'collection_name'].values[1],
                      'count_collections': data.loc[data['collection_name'].str.contains(regex, regex=True), 'id'].count().item(),
                      'total_gain': data.loc[data['collection_name'].str.contains(regex, regex=True), 'revenue'].sum().item(),
                      'mean_gain': data.loc[data['collection_name'].str.contains(regex, regex=True), 'revenue'].mean().item()}
        return franchise_data
    except:
        return 'The inputed collection its not part of a collection.'

@app.get('/peliculas_pais/{country}')
def movies_per_country(country: str):
    data['prod_countries'].fillna('', inplace = True)
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
    data['prod_companies'].fillna('', inplace = True)
    try:
        company_data = {'company': company,
                    'total_movies': data.loc[data['prod_companies'].str.contains(regex, regex=True), 'id'].count().item(),
                    'total_revenue': data.loc[data['prod_companies'].str.contains(regex, regex=True), 'revenue'].sum().item()}
        return company_data
    except:
        return {'There is no company with the name that you ingresed in the database'}

@app.get('/get_director/{director}')
def director_data(director: str):
    data['directors'].fillna('', inplace = True)
    regex = re.compile(director, re.IGNORECASE)
    try:
        movies_data_list = []
        movies_data_list = []
        director_df = data.loc[data['directors'].str.contains(regex, regex=True)].values
        for i in range(len(director_df)):
            movies_data_list.append([])
            movies_data_list[i] = {'title': director_df[i][4],
                                    'release_date': director_df[i][10],
                                    'budget': str(director_df[i][17]),
                                    'revenue': str(director_df[i][18]),
                                    'return': str(director_df[i][19])}
            director_data = {'director':regex,
                            'total_movies_return': str(round(data.loc[data['directors'].str.contains(regex, regex=True), 'return'].sum().item(),2)),
                            'produced_movies': movies_data_list}
        return(director_data)
    except:
         return('There is no director with that name')
    
@app.get('/recomendacion/{title}')
def recommendation(title: str):
    index = reduced_data[reduced_data['title'] == title].index[0]
    #Make a index-similarity matrix
    sim_scores = list(enumerate(cosine_sim[index]))
    #Sort the scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #Recomend the first 5 movies with the most similarity
    top_recommendations = []
    for i in range(1,6):
        top_recommendations.append([])
        top_recommendations[i-1] = {'title':reduced_data.iloc[sim_scores[i][0]].title, 
                            'vote_average': str(reduced_data.iloc[sim_scores[i][0]].vote_average), 
                            'genres_list': reduced_data.iloc[sim_scores[i][0]].genres_list,
                            'directors': reduced_data.iloc[sim_scores[i][0]].directors}
    return {"title": str(title), "recommendations": top_recommendations}
