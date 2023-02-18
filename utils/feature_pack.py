import datetime
import json
import random

from utils import config

def get_str_time() -> str:
    hour = datetime.datetime.now().hour

    if 0 <= hour and hour < 6:
        return "Night"
    elif 6 <= hour and hour < 12:
        return "Morning"
    elif 12 <= hour and hour < 18:
        return "Afternoon"
    elif 18 <= hour and hour < 24:
        return "Evening"
    else:
        return "Day"

def get_featured_movies() -> list:
    path_to_featured = "static/data/featured_movies/movies.json"
    with open(config.PROJECT_DIR + path_to_featured) as f:
        parsed_data = json.loads(f.read())
        parsed_data = parsed_data.get("movies")

        random.seed(datetime.datetime.now().microsecond)
        random_selections = random.sample(
            range(0, len(parsed_data)), 3)

        random_movies = []
        for i in range(3):
            random_movies.append(
                parsed_data[random_selections[i]]
            )

        return random_movies

def get_profile_picture() -> str:
    path_to_pics = "static/data/profile_pictures/profile_pictures.json"
    with open(config.PROJECT_DIR + path_to_pics) as f:
        parsed_data = json.loads(f.read())
        parsed_data = parsed_data.get("profile_pictures")

        random.seed(datetime.datetime.now().microsecond)
        random_index = random.randint(0, (len(parsed_data) - 1))

        return parsed_data[random_index].get("path")

if __name__ == "__main__":
    #print(get_featured_movies())
    print(get_profile_picture())
