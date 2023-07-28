import os
import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv() # do this immediately so any code after can run environment variables

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
); """

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHLIST_TABLE="""CREATE TABLE IF NOT EXISTS watched(
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY (user_username) REFERENCES users(username),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s,%s);"
INSERT_NEW_USER = "INSERT INTO users (username) VALUES (%s);"
SELECT_ALL_MOVIES = 'SELECT * FROM movies;'
SELECT_UPCOMING_MOVIES = 'SELECT * FROM movies WHERE release_timestamp > %s;'
SELECT_WATCHED_MOVIES = """ SELECT * FROM movies
JOIN watched ON watched.movie_id = movies.id
JOIN users ON users.username = watched.user_username
WHERE users.username = %s;
"""
DELETE_MOVIE = 'DELETE FROM movies WHERE title = %s;'
INSERT_WATCHED_MOVIE = 'INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);'
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = %s;"
SEARCH_MOVIES = 'SELECT * FROM movies WHERE title LIKE %s;'

connection = psycopg2.connect(os.environ['DATABASE_URL'])

def search_movies(search_term):
    with connection:
        # in postgre, we always need cursors
        with connection.cursor() as cursor:
            return cursor.execute(SEARCH_MOVIES, (f'%{search_term}%',))

def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHLIST_TABLE)

def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES,(title, release_timestamp))

def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_NEW_USER, (username,))


def get_movies(upcoming = False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today = datetime.datetime.today().timestamp()
                return cursor.execute(SELECT_UPCOMING_MOVIES,(today,)) #(today,) needs to be a tuple which is why we insert ,
            else:
                return cursor.execute(SELECT_ALL_MOVIES)

def get_watched_movies(username):
    with connection:
        with connection.cursor() as cursor:
            return cursor.execute(SELECT_WATCHED_MOVIES, (username,))

def watch_movie(username, movie_id):
#    query = 'UPDATE movies SET watched = 1 WHERE title = ?'
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))
