from fetch_files import download_files
download_files()  # will download both files if not already present
import pickle
movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))


import streamlit as st
import requests


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=34321fe4df1284151229782506a2e606&language=en-US"
        response = requests.get(url)
        data = response.json()

        # Safely fetch poster_path
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Loading"


def recommend(movie, num_results):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:num_results + 1]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header('Movie Recommender System')

# Load data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

num_recommendations = st.slider("Select number of recommendations", min_value=1, max_value=20, value=5)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie, num_recommendations)

    for i in range(0, num_recommendations, 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < num_recommendations:
                with cols[j]:
                    st.text(names[i + j])
                    st.image(posters[i + j])

st.markdown(f"You selected **{num_recommendations}** recommendations.")