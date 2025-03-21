import streamlit as st
import pandas as pd
import pickle
import requests
import gzip
import os



def fetch_poster(movie_id):
    api_key = "a3f15063654a9486ab757268ffd30e04"  
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    response = requests.get(url)
    data = response.json()

    if "poster_path" in data and data["poster_path"]:  
        return f"http://image.tmdb.org/t/p/w500{data['poster_path']}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"  



def recommend(movie):
    movie = movie.lower().strip()

    if movie not in movies['title'].str.lower().values:
        return ["Movie not found! Please enter a valid movie name."], []

    movie_index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters



movies_dict = pickle.load(open('movie_dict.pkl', "rb"))
movies = pd.DataFrame(movies_dict)


similarity = None
if os.path.exists('similarity.pkl.gz'):
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)
elif os.path.exists('similarity.pkl'): 
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
else:
    st.error("Error: similarity.pkl.gz or similarity.pkl file not found!")

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

   
    cols = st.columns(5)

   
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

  
    if len(recommended_movie_names) > 5:
        cols = st.columns(5)
        for i in range(5, len(recommended_movie_names)):
            with cols[i - 5]:  
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
