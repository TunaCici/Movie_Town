from custom_mongo.mongo_handler import MongoHandler
from custom_elastic.elastic_handler import ElasticHandler
from utils import handler

if __name__ == "__main__":
    mongo_inst = MongoHandler()
    elastic_inst = ElasticHandler()

    if not mongo_inst.running():
        print("Failed to connect to MongoDB server.")
        exit(-1)
    
    if not elastic_inst.running():
        print("Failed to connect to ElasticSearch server.")
        exit(-1)

    print("Adding movies to MongoDB.")
    # mongo_inst.init_movies()
    print("Added movies to MongoDB.")

    print("Adding movies to ElasticSearch.")
    handler.check_integrity(mongo_inst, elastic_inst, 0, 100000)
    print("Added movies to ElasticSearch.")