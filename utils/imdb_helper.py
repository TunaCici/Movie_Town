"""
Author: Tuna Cici
Written on: 23/08/2021

What is this:
This utilty provides siple interface
to imdb files such as, movies, actors.
"""

from io import FileIO
import json
from numpy import int64
import pandas as pd
import logger
import config

FILE_MOVIES: FileIO
FILE_NAMES: FileIO
FILE_RATINGS: FileIO
FILE_TITLE_PRINCIPALS: FileIO
IMDB_LOGGER = logger.CustomLogger()

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
    print("")

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

if __name__ == "__main__":
    IMDB_LOGGER.log_info("Started main function.")
    open_files()

    hey = get_with_index(FILE_MOVIES, 15)