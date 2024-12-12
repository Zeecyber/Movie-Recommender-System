from flask import Flask, flash
import pymysql
import pickle
import pandas as pd
import requests
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
# MySQL Database connection details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'movierecommenderdb'

# Create a connection to MySQL using pymysql
def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Define the database models manually
def get_user_by_email(email):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
        user = cursor.fetchone()
    connection.close()
    return user

def insert_user(username, email, password_hash):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO users (Username, Email, PasswordHash) VALUES (%s, %s, %s)", 
                       (username, email, password_hash))
        connection.commit()
    connection.close()

def get_user_by_id(user_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
    connection.close()
    return user

def insert_search_history(user_id, selected_movie):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO SearchHistory (UserID, SearchQuery) VALUES (%s, %s)", 
                           (user_id, selected_movie))
            connection.commit()
        flash(f"Search for '{selected_movie}' added to history!", "success")
    except Exception as e:
        flash(f"An error occurred while processing your search: {e}", "error")
    finally:
        connection.close()


API_KEY = "0d5c7b359864932b1dba2bd802b1653e"
movies_list = pickle.load(open(r'D:\code\Movie Recommender System\move.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open(r'D:\code\Movie Recommender System\similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [(movies.iloc[i[0]].title, fetch_poster(movies.iloc[i[0]].movie_id)) for i in distances[1:11]]
    return recommended_movies

def History_display(title):
    result = movies[movies['title'] == title]
    if not result.empty:
        poster_url = fetch_poster(result.iloc[0]['movie_id'])
        return (title, poster_url)
    return (title, '')
