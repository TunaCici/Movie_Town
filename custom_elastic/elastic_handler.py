import elasticsearch
import uuid

URL = "localhost"
PORT = 9200

AUTH_ID = "elastic"
AUTH_PASS = "QQr9ElJyJOh0MAD27ZEH"

INDEX_NAME = "movie_town"

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
            hosts=URL, port=PORT,
            http_auth=(AUTH_ID, AUTH_PASS)) 

        # check the connection
        if self.client.ping():
            self.is_running = True
        else:
            print("Elasticsearch server not available.")
            self.is_running = False
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
        self.is_running = self.client.ping()
        return self.is_running

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

            result = response.get("hits").get("hits")[0]

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
    elastic_test = ElasticHandler()
    print(elastic_test.running())

    test_indexing = False
    if test_indexing:
        result = elastic_test.movie_add(
            "tt00000010", "Miss Jerry",
            "1894", "Romance",
            "45", "USA",
            "Alexander Black", "Alexander Black",
            "Alexander Black Photoplays", "Blanche Bayliss, William Courtenay, Chauncey Depew",
            "The adventures of a female reporter in the 1890s.", 5.9,
            "no_path"
        )
        print(result)
    
    test_deleting = False
    if test_deleting:
        result = elastic_test.movie_delete("0ed13bd0-a9c5-4502-b568-fda56a9049e5")
        print(result)

    test_searching = False
    if test_searching:
        result = elastic_test.search("jerry")
        print(result)

    test_get = False
    if test_get:
        result = elastic_test.movie_get("c21243c6-0ac9-467c-96bb-335cc7a2c7f0")
        print(result)