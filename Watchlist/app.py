import datetime
import database


menu = """\nPlease select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Add user.
7) Search for a movie.
8) Exit. 

Your selection:  """

welcome = "Welcome to the watchlist app!"

print(welcome)
database.create_tables()

def prompt_add_movie():
    title = input('Movie title: ')
    release_date = input('Release date (dd-mm-YYYY): ')
    #date time object that is parsed
    # TIMESTAMP DOES NOT WORK IF DATE LESS THAN OR EQUAL TO January 1, 1970
    parsed_date = datetime.datetime.strptime(release_date, '%d-%m-%Y')
    print(type(title))
    print(type(parsed_date.timestamp()))
    database.add_movie(title, parsed_date.timestamp())

def print_movie_list(movies):
    print('-- Upcoming Movies --')
    for m in movies:
        print(f'{m}\n')

def print_watched_movie_list(username, movies):
    print(f"{username}'s watched movies\n")
    for m in movies:
        print(m)

def prompt_watch_movie():
    username = input('Who watched: ')
    movie_id = input('What movie did you watch: ')
    database.watch_movie(username, movie_id)

def prompt_search_movies():
    movie_title = input('Which movie:')
    print_movie_list(database.search_movies(movie_title))

while (user_input := input(menu)) != "8":
    if user_input == '1':
        prompt_add_movie()
    elif user_input == '2':
        print_movie_list(database.get_movies())
    elif user_input == '3':
        print_movie_list(database.get_movies())
    elif user_input == '4':
        prompt_watch_movie()
    elif user_input == '5':
        username = input('Who watched: ')
        print(print_watched_movie_list(username, database.get_watched_movies(username)))
    elif user_input == '6':
        username = input('Name of User:')
        database.add_user(username)
    elif user_input == '7':
        prompt_search_movies()
    else:
        print('Invalid input, please try again!')
