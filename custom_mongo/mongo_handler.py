import pymongo
import bcrypt
import uuid
from pymongo import database
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

URL = "localhost"
PORT = 27017

DB_NAME = "movie_town"
USER_COLLECTION_NAME = "users"
MOVIE_COLLECTION_NAME = "movies"

user_struct = {
    "u_id": uuid.UUID,
    "u_name": str,
    "u_surname": str,
    "u_username": str,
    "u_mail": str,
    "u_password": bytes
}

movie_struct = {
    "m_id": None,
    "m_imdb_id": None,
    "m_title": None,
    "m_year": None,
    "m_genre": None,
    "m_duration": None,
    "m_country": None,
    "m_director": None,
    "m_writer": None,
    "m_actors": None,
    "m_description": None,
    "m_score": None,
    "m_poster": None
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
        self, id: uuid.UUID, name: str,
        surname: str, username: str,
        mail: str, password: bytes ) -> bool:
        user_struct = {
            "u_id": id,
            "u_name": name,
            "u_surname": surname,
            "u_username": username,
            "u_mail": mail,
            "u_password": password
        }
        try:
            self.user_collection.insert_one(user_struct)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

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

    def user_get(self, username: str) -> dict:
        try:
            res = self.user_collection.find_one({"u_username": username})
            return res
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

if __name__ == "__main__":
    inst = MongoHandler()
    res = inst.user_get("miketheking")
