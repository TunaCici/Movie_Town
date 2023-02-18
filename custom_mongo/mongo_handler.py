import datetime
import time
import numpy
import uuid
import json
import sys
import pandas as pd
from pymongo import database
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

sys.path.append("..")
from utils import config

# connection and authentication info
HOST = "localhost"
PORT = 27017
USERNAME = "mongo"
PASSWORD = "Eqqz6fXGyhXTpmN8"

if USERNAME and PASSWORD:
    CONNECTION_STRING = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
else:
    CONNECTION_STRING = f"mongodb://{HOST}:{PORT}"

# database releated info
DB_NAME = "movie_town"
USER_COLLECTION_NAME = "users"
MOVIE_COLLECTION_NAME = "movies"
WATCHLIST_COLLECTION_NAME = "watchlist"

# general info
MAX_RECONNECT_COUNT = 30 # times
CONNECTION_TIMEOUT = 1000 # miliseconds

user_struct = {
    "u_id": uuid.UUID,
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

watchlist_struct = {
    "u_id": uuid.UUID,
    "u_watchlist": str,
    "u_remindertime": datetime.datetime
}

class MongoHandler:
    is_running = False
    client: MongoClient

    db: database.Database
    user_collection: database.Collection
    movie_collection: database.Collection
    watchlist_collection: database.Collection

    def __init__(self):
        print("Starting a new Mongo client.")
        print(f"Host: {HOST}, Port: {PORT}")
        try:
            self.client = MongoClient(
                CONNECTION_STRING, serverSelectionTimeoutMS=CONNECTION_TIMEOUT)
        except ConnectionFailure as e:
            print(e)
            print("Connection failed. See the above details.")
            return None
        
        # just in case check the connection again
        if not self.running():
            print("Connection failed.")
            return None

        # create database and collections
        self.db = self.client[DB_NAME]
        self.user_collection = self.db[USER_COLLECTION_NAME]
        self.movie_collection = self.db[MOVIE_COLLECTION_NAME]
        self.watchlist_collection = self.db[WATCHLIST_COLLECTION_NAME]
        print("MongoDB initialization successful.")

    def running(self) -> bool:
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            return True
        except ConnectionFailure:
            print("Connection dropped.")
            i = 1
            while i <= MAX_RECONNECT_COUNT:
                print(f"Trying to reconnect [{i}/{MAX_RECONNECT_COUNT}]")

                try:
                    self.client = MongoClient(
                        CONNECTION_STRING, serverSelectionTimeoutMS=CONNECTION_TIMEOUT)
                    self.client.admin.command('ismaster')
                    print("Successfully reconnected.")
                    return True
                except ConnectionFailure:
                    i += 1

            return False

    def get_mongo(self) -> MongoClient:
        return self.client

    def list_databases(self) -> None:
        dbs = self.client.list_database_names()
        print(dbs)

    def user_add(
        self, name: str, surname: str,
        username: str, mail: str,
        password: str, picture: str ) -> bool:

        # create unique id for the user
        unique_id = uuid.uuid4()
        unique_id = str(unique_id)

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
            self.watchlist_add(unique_id)
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

    def user_delete(self, id: str):
        try:
            res = self.user_collection.find_one({"u_id": id})
            if res:
                self.user_collection.delete_one({"u_id": id})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def user_update_name(self, id: str, name: str):
        try:
            self.user_collection.update_one(
                {"u_id": id},
                {"$set": {"u_name": str(name)}})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None
    
    def user_update_mail(self, id: str, mail: str):
        try:
            self.user_collection.update_one(
                {"u_id": id},
                {"$set": {"u_mail": str(mail)}})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def user_update_password(self, id: str, password: str):
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

    def watchlist_add(self, id: str):
        watchlist_struct = {
            "u_id": id,
            "u_watchlist": "None",
            "u_remindertime": datetime.datetime.now()
        }
        try:
            self.watchlist_collection.insert_one(watchlist_struct)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return False

    def watchlist_get(self, id: str) -> list:
        try:
            res = self.watchlist_collection.find_one({"u_id": id})
            watch_list = res.get("u_watchlist", "None")

            
            if (watch_list == "None") or (watch_list is None):
                return []
            
            parsed_list = json.loads(watch_list)
            return parsed_list.get("list")
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def watchlist_update(self, id: str, new_list: str):
        try:
            self.watchlist_collection.update_one(
                {"u_id": id},
                {"$set": {"u_watchlist": str(new_list)}})
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None
    
    def watchlist_update_reminder(self, id: str, date: datetime.datetime):
        try:
            self.watchlist_collection.update_one(
                {"u_id": id},
                {"$set": {"u_remindertime": date}})
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

                total_movies = df.shape[0]
                total_done = 0
                
                for i in df.to_dict("records"):
                    if total_done % 1000 == 0:
                        print(f"Movies added {total_done}/{total_movies}")
                    
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
                    total_done += 1
    
                print(f"Movies added {total_done}/{total_movies}")
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
    print("Creating an instance of Mongo handler.")
    inst = MongoHandler()
    
    if not inst:
        print("Failed to create an instance. Exiting.")
        exit(-1)
    
    while True:
        print("***********************")
        print("1. Check connection")
        print("2. List all dbs")
        print("3. Init movies")
        print("0. Exit")
        print("***********************")
        op = input('Enter operation no: ')
        if op == "0":
            exit(0)
        elif op == "1":
            if inst.running():
                print("Connection is active.")
            else:
                print("Connection is inactive.")
        elif op == "2":
            inst.list_databases()
        elif op == "3":
            inst.init_movies()
        else:
            print("Invalid operation, try again.")