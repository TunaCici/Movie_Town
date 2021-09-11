from numpy import str_
import pymongo
import bcrypt
import numpy
import uuid
import sys
import pandas as pd
from pymongo import database
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

sys.path.append("..")
from utils import config

URL = "localhost"
PORT = 27017

DB_NAME = "movie_town"
USER_COLLECTION_NAME = "users"
MOVIE_COLLECTION_NAME = "movies"

user_struct = {
    "u_id": str_,
    "u_name": str,
    "u_surname": str,
    "u_username": str,
    "u_mail": str,
    "u_password": bytes,
    "u_picture": str
}

movie_struct = {
    "m_id": str,
    "m_imdb_id": str,
    "m_title": str,
    "m_year": str,
    "m_genre": str,
    "m_duration": str,
    "m_country": str,
    "m_director": str,
    "m_writer": str,
    "m_production": str,
    "m_actors": str,
    "m_description": str,
    "m_score": float,
    "m_poster": str
}

class MongoHandler:
    is_running = False
    client: MongoClient

    db: database.Database
    user_collection: database.Collection
    movie_collection: database.Collection

    def __init__(self):
        self.client = MongoClient(host=URL, port=PORT)
        try:
        # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            print("MongoDB server not available.")
            self.is_running = False
            return None
        self.is_running = True
        
        # create database and collections
        self.db = self.client[DB_NAME]
        self.user_collection = self.db[USER_COLLECTION_NAME]
        self.movie_collection = self.db[MOVIE_COLLECTION_NAME]
        print("MongoDB initialization successful.")

    def running(self) -> bool:
        try:
        # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            print("Server not available.")
            self.is_running = False
        self.is_running = True
        
        return self.is_running

    def get_mongo(self) -> MongoClient:
        return self.client

    def user_add(
        self, name: str, surname: str,
        username: str, mail: str,
        password: bytes, picture: str ) -> bool:

        # create unique id for the user
        unique_id = uuid.uuid4()

        user_struct = {
            "u_id": unique_id,
            "u_name": name,
            "u_surname": surname,
            "u_username": username,
            "u_mail": mail,
            "u_password": password,
            "u_picture": picture
        }
        try:
            self.user_collection.insert_one(user_struct)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return False

        return True

    def username_exists(self, username: str) -> bool:
        try:
            res = self.user_collection.find_one({"u_username": username})
            if res is None:
                return False
            return True
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None


    def mail_exists(self, mail: str) -> bool:
        try:
            res = self.user_collection.find_one({"u_mail": mail})
            if res is None:
                return False
            return True
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def user_delete(self, id: uuid.UUID):
        try:
            res = self.user_collection.find_one({"u_id": id})
            if res:
                self.user_collection.delete_one({"u_id": id})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def user_update_name(self, id: uuid.UUID, name: str):
        try:
            self.user_collection.update_one(
                {"u_id": id},
                {"$set": {"u_name": str(name)}})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None
    
    def user_update_mail(self, id: uuid.UUID, mail: str):
        try:
            self.user_collection.update_one(
                {"u_id": id},
                {"$set": {"u_mail": str(mail)}})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def user_update_password(self, id: uuid.UUID, password: bytes):
        try:
            self.user_collection.update_one(
                {"u_id": id},
                {"$set": {"u_password": password}})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def user_get(self, username: str) -> dict:
        try:
            res = self.user_collection.find_one({"u_username": username})
            return res
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None
    
    def init_movies(self):
        try:
            with open(config.PROJECT_DIR + "data/imdb_movies.csv") as movie_file:
                pd_csv = pd.read_csv(movie_file, low_memory=False)
                df = pd.DataFrame(pd_csv)
                df = df.replace({numpy.nan: None})

                for i in df.to_dict("records"):
                    movie_struct = {
                        "m_id": i.get("id", "None"),
                        "m_imdb_id": i.get("imdb_title_id", "None"),
                        "m_title": i.get("title", "None"),
                        "m_year": i.get("year", "None"),
                        "m_genre": i.get("genre", "None"),
                        "m_duration": i.get("duration", 0),
                        "m_country": i.get("country", "None"),
                        "m_director": i.get("director", "None"),
                        "m_writer": i.get("writer", "None"),
                        "m_production": i.get("production_company", "None"),
                        "m_actors": i.get("actors", "None"),
                        "m_description": i.get("description", "None"),
                        "m_score": i.get("avg_vote", 0.0),
                        "m_poster": i.get("poster_path", "None")
                    }
                    self.movie_collection.insert_one(movie_struct)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def get_range_of_movies(self, start: int, end: int) -> list:
        if start < 0 or end < 0:
            print("Range values cannot be smaller than 0")
            return None

        movies: list

        try:
            movies = self.movie_collection.find().skip(start).limit(end)
            return list(movies)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None       
    
    def movie_get_count(self) -> int:
        try:
            return self.movie_collection.count()
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

if __name__ == "__main__":
    inst = MongoHandler()
    
    inst.init_movies()