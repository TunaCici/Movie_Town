
import redis
from redis import Redis
from typing import Any

URL = "localhost"
PORT = 6379

class RedisHandler:
    is_running = False
    client: Redis

    def __init__(self):
        self.client = redis.Redis(host=URL, port=PORT)

        if self.client.ping():
            self.is_running = True
        else:
            self.is_running = False
            print("Server not available.")
            
        print("Initialization successful.")

    def runnig(self) -> bool:
        if self.client.ping():
            self.is_running = True
        else:
            self.is_running = False
            
        return self.is_running
    
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

    inst.reset()
