import time
from redis import Redis
from typing import Any

# connection and authentication info
HOST = "localhost"
PORT = 6379

# general info
MAX_RECONNECT_COUNT = 30 # times

class RedisHandler:
    is_running = False
    client: Redis

    def __init__(self):
        try:
            self.client = Redis(host=HOST, port=PORT)
            print("Connected to Redis server.")
        except Exception as e:
            print(e)
            print("Connection failed. See the above details.")
            return None

        if not self.running():
            print("Connection failed.")
            return None    

    def running(self) -> bool:
        try:
            if self.client.ping():
                return True
            return False
        except Exception as e:
            print("Connection dropped.")
            i = 1
            while i <= MAX_RECONNECT_COUNT:
                print(f"Trying to reconnect [{i}/{MAX_RECONNECT_COUNT}]")
                try:
                    self.client = Redis(host=HOST, port=PORT) 
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

    def get_redis(self) -> Redis:
        return self.client

    def cache(self, keyword: str, value: Any):
        try:
            self.client.set(keyword, value)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None
    
    def retrieve(self, keyword: str):
        try:
            self.client.get(keyword)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None
    
    def reset(self):
        try:
            self.client.flushall()
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

    def delete(self, keyword: str):
        try:
            self.client.delete(keyword)
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None

if __name__ == "__main__":
    inst = RedisHandler()

    if not inst:
        print("Failed to create an instance. Exiting.")
        exit(-1)

    while True:
        print("***********************")
        print("1. Check connection")
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
        else:
            print("Invalid operation, try again.")