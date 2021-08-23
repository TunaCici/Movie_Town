"""
Author: Tuna Cici

What is this:
This utilty script gets movie and tv show
data from the IMDb servers. 
"""

from imdb import IMDb

if __name__ == "__main__":
    print("Started as main.")

    ia = IMDb()

    for i in range(9999999):
        movie = None
        try: 
            movie = ia.get_movie(i)
        except:
            print("Bruh")
        print(movie)