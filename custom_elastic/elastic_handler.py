import elasticsearch
import uuid
import time

# connection and authentication info
HOST = "localhost"
PORT = 9200
USERNAME = ""
PASSWORD = ""

# database releated info
INDEX_NAME = "movie_town"

# general info
MAX_RECONNECT_COUNT = 30 # times

SEARCH_FIELDS = [
    "m_imdb_id",
    "m_title",
    "m_year",
    "m_director",
    "m_writer",
    "m_production",
    "m_actors",
    "m_description",
    "m_description"
]

class ElasticHandler():
    is_running = False
    client = elasticsearch.Elasticsearch

    def __init__(self):
        self.client = elasticsearch.Elasticsearch(
            hosts=HOST, port=PORT,
            http_auth=(USERNAME, PASSWORD)) 

        # just in case check the connection again
        if not self.running():
            print("Elasticsearch server not available.")
            return None

        # create indices if not exists
        if not self.client.indices.exists(index=INDEX_NAME):
            try:
                self.client.indices.create(index=INDEX_NAME, ignore=400)
            except Exception as e:
                print("An error occured operation will stop. See details:")
                print(e)
                return None
        
        print("Elasticsearch initialization successful.")

    def running(self) -> bool:
        if self.client.ping():
            return True

        print("Connection dropped.")
        i = 1
        while i <= MAX_RECONNECT_COUNT:
            print(f"Trying to reconnect [{i}/{MAX_RECONNECT_COUNT}]")
            try:
                self.client = elasticsearch.Elasticsearch(
                    hosts=HOST, port=PORT,
                    http_auth=(USERNAME, PASSWORD)) 
                if self.client.ping():
                    print("Successfully reconnected.")
                    return True
                else:
                    i += 1
                    time.sleep(1)
            except Exception as e:
                i += 1
                time.sleep(1)

        return False

    def get_elastic(self) -> elasticsearch.Elasticsearch:
        return self.client

    def movie_add(
        self, unique_id: str, imdb_id: str,
        title: str, year: str,
        genre: str,duration: str,
        country: str, director: str,
        writer: str, production: str,
        actors: str, description: str,
        score: float, poster: str
    ):
        movie_struct = {
            "m_id": unique_id,
            "m_imdb_id": imdb_id,
            "m_title": title,
            "m_year": year,
            "m_genre": genre,
            "m_duration": duration,
            "m_country": country,
            "m_director": director,
            "m_writer": writer,
            "m_production": production,
            "m_actors": actors,
            "m_description": description,
            "m_score": score,
            "m_poster": poster
        }

        # index the movie
        try:
            self.client.index(
                index=INDEX_NAME,
                body=movie_struct,
                id=unique_id,
                refresh=True
            )
        except Exception as e:
            print("[ELASTIC] An error occured when adding movie. See details:")
            print(e)
            return False
        
        return True
    
    def movie_delete(self, target_id: str) -> bool:
        try:
            self.client.delete(
                index=INDEX_NAME,
                id=target_id,
                refresh=True
            )
            return True

        except elasticsearch.NotFoundError as e:
            print(f"Could not find user with id: {target_id}")
            return False

        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return False

    def movie_get(self, target_id: str) -> dict:
        search_query = {
            "_source": True,
            "size": 1,
            "query": {
                "match": {
                    "_id": target_id
                }
            }
        }
        
        try:
            response = self.client.search(
                index=INDEX_NAME,
                body=search_query
            )

            result_size = response.get("hits").get("total").get("value")
            if result_size == 0:
                return []

            result = response.get("hits").get("hits")[0].get("_source")

            return result
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return False


    def search(self, search_str: str) -> list:
        # limit searching for safety(?) and performance
        if 32 <= len(search_str):
            print("Search string cannot be greater then 32 characters.")
            return None

        # query for searching
        search_query = {
            "_source": True,
            "size": 3,
            "query": {
                "multi_match": {
                    "query": search_str,
                    "fields": SEARCH_FIELDS
                }
            }
        }

        try:
            response = self.client.search(
                index=INDEX_NAME,
                body=search_query
            )

            # get size of results
            result_size = response.get("hits").get("total").get("value")
            if result_size == 0:
                return []
            
            # obtain results
            result_list: list = response.get("hits").get("hits")

            # obtain movies from the result
            parsed_list = [i.get("_source") for i in result_list]

            return parsed_list
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return False

if __name__ == "__main__":
    inst = ElasticHandler()

    if not inst:
        print("Failed to create an instance. Exiting.")
        exit(-1)

    while True:
        print("***********************")
        print("1. Check connection")
        print("2. Check indexing")
        print("3. Check searching")
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
            result = inst.movie_add(
                "this-is-a-cool-uuid",
                "tt00000010",
                "Miss Jerry",
                "1894", "Romance",
                "45", "USA",
                "Alexander Black", "Alexander Black",
                "Alexander Black Photoplays", "Blanche Bayliss, William Courtenay, Chauncey Depew",
                "The adventures of a female reporter in the 1890s.", 5.9,
                "no_path" 
            )
            print(result)
        elif op == "3":
            result = inst.search("jerry")
            print(result)
        else:
            print("Invalid operation, try again.")
        