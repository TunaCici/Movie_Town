"""
Author: Tuna Cici
Written on: 23/08/2021

What is this:
This utilty provides simple interface
to imdb files such as, movies, actors.
"""

import json
import os
import requests
import pandas as pd
from io import FileIO
from numpy import int64

if __name__ == "utils." + os.path.basename(__file__)[:-3]:
    # importing from outside the package
    from utils import config
    from utils import logger
else:
    # importing from main and inside the package
    import config
    import logger


FILE_MOVIES: FileIO
FILE_NAMES: FileIO
FILE_RATINGS: FileIO
FILE_TITLE_PRINCIPALS: FileIO
IMDB_LOGGER = logger.CustomLogger()

TMDB_API_SESSION = requests.session()
TMDB_IMG_SESSION = requests.session()

def open_files():
    global FILE_MOVIES
    global FILE_NAMES
    global FILE_RATINGS
    global FILE_TITLE_PRINCIPALS

    IMDB_LOGGER.log_info("Opening files...")
    FILE_MOVIES = open(config.PROJECT_DIR + "data/imdb_movies.csv", encoding="utf8")
    FILE_NAMES = open(config.PROJECT_DIR + "data/imdb_names.csv", encoding="utf8")
    FILE_RATINGS = open(config.PROJECT_DIR + "data/imdb_ratings.csv", encoding="utf8")
    FILE_TITLE_PRINCIPALS = open(config.PROJECT_DIR + "data/imdb_title_principals.csv", encoding="utf8")
    IMDB_LOGGER.log_info("Files opened.")

def close_files():
    global FILE_MOVIES
    global FILE_NAMES
    global FILE_RATINGS
    global FILE_TITLE_PRINCIPALS

    IMDB_LOGGER.log_info("Closing files...")
    FILE_MOVIES.close()
    FILE_NAMES.close()
    FILE_RATINGS.close()
    FILE_TITLE_PRINCIPALS.close()
    IMDB_LOGGER.log_info("Files closed.")

def print_all(file: str):
    """
    Options: movies, names, ratings, principals
    """
    pd_file = pd.read_csv(file, low_memory=False)
    df = pd.DataFrame(pd_file)
    print(df)

def get_with_index(file: FileIO, index : int) -> dict:
    """
    Get's the data stated by the index from the file.
    Returns it as dict.
    """

    if index < 0:
        IMDB_LOGGER.log_warning("Index must be greater than 0.")
        return
    
    # dataframe
    df = pd.read_csv(file, low_memory=False)

    # list of columns
    cl = df.columns

    return_value = {}

    # get the data from file to a dict
    for i in cl:
        if type(df[i][index]) is int64:
            return_value[i] = int(df[i][index])
        else:
            return_value[i] = df[i][index]
       
    return return_value

def get_columns(file: FileIO) -> list:
    """
    Returns all the columns in a file as a list.
    """
    df = pd.read_csv(file, low_memory=False)
    return df.columns

def get_image(imdb_id: str) -> bytes:
    api_key = "fe0c11c0aeee82176ba4b9f31e43b286"
    url = "https://api.themoviedb.org/3/find/" + imdb_id +"?api_key=" + api_key + "&external_source=imdb_id"

    response = TMDB_API_SESSION.get(url)
    if response.status_code == 200:
        results = response.json()["movie_results"]

        # no movie was found
        if len(results) == 0:
            print(f"could not found the movie: {imdb_id}")
            return None

        path = results[0]["poster_path"]
        # no poster was found
        if path is None:
            print(f"no poster found.")
            return None
        
        img_data = TMDB_IMG_SESSION.get("https://image.tmdb.org/t/p/original" + path).content
        return img_data
    else:
        print("an error occured.")
        return None

def init_movie_images():
    pd_file = pd.read_csv(FILE_MOVIES, low_memory=False)
    df = pd.DataFrame(pd_file)

    # list all images in data/posters folder
    curr_posters = os.listdir(config.PROJECT_DIR + "data/posters")
    
    for imdb_id in df["imdb_title_id"]:
        print(f"looking for: {imdb_id}")
        file_name = imdb_id + ".jpg"
        if file_name in curr_posters:
            print("Poster already exists.")
        else:
            img_data = get_image(str(imdb_id))
            if img_data is not None:
                with open(config.PROJECT_DIR + "data/posters/" + imdb_id + ".jpg", "wb") as f:
                    f.write(img_data)
                print(f"Save {file_name}")

def drop_column(file: FileIO, columns: list):
    pd_file = pd.read_csv(file, low_memory=False)
    df = pd.DataFrame(pd_file)
    df.drop(columns, axis=1, inplace=True)
    df.to_csv("imdb_movies.csv", encoding="utf8")

if __name__ == "__main__":
    IMDB_LOGGER.log_info("Started main function.")
    open_files()
    hey = get_with_index(FILE_MOVIES, 56)
    close_files()

    open_files()
    init_movie_images()
    close_files()