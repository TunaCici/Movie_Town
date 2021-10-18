from custom_mongo.mongo_handler import MongoHandler

if __name__ == "__main__":
    inst = MongoHandler()

    if not inst.running():
        print("Failed to connect to MongoDB server.")
        exit(-1)
    
    inst.init_movies()