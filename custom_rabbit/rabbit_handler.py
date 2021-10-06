import pika
import json
import time
import threading

from pika.adapters.blocking_connection import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from pika.spec import Basic
from pika.spec import BasicProperties

URL = "localhost"
PORT = 5672

REQUEST_QUEUE_NAME = "request_queue"
RESULT_QUEUE_NAME = "result_queue"

request_queue_struct = {
    "operation": str,
    "data": list,
    "extra": None
}

result_queue_struct = {
    "result": str,
    "data": None,
    "extras": None
}

class RabbitHandler():
    is_running = False
    client: BlockingConnection
    channel: BlockingChannel
    channel_number: int

    def __init__(self):
        # establish the connection
        try:
            self.client = BlockingConnection(
                pika.ConnectionParameters(host=URL, port=PORT))
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return None
        
        # check the connection
        if not self.client.is_open:
            print("RabbitMQ server not available.")
            self.is_running = False
            return None
        
        # intialize channel
        self.channel = self.client.channel()
        self.channel_number= self.channel.channel_number

        # initialize queues
        self.channel.queue_declare(REQUEST_QUEUE_NAME)
        self.channel.queue_declare(RESULT_QUEUE_NAME)
        
        self.is_running = True

    def running(self) -> bool:
        self.is_running = self.client.is_open
        return self.is_running

    def get_channel_number(self) -> int:
        return self.channel_number
    
    def request_add(
        self, owner: str, operation: str, data: str, extras) -> bool:
        request_queue_struct = {
            "owner": owner,
            "operation": operation,
            "data": data,
            "extras": extras
        }

        request_body = json.dumps(request_queue_struct)

        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=REQUEST_QUEUE_NAME,
                body=request_body)
            print(f"Adding request: {request_body}")
            return True
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return False

    def result_add(
        self, owner: str, operation: str, 
        result: str, data: str, extras) -> bool:
        result_queue_struct = {
            "owner": owner,
            "operation": operation,
            "result": result,
            "data": data,
            "extras": extras
        }

        result_body = json.dumps(result_queue_struct)

        print(f"Adding result: {result_body}")

        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=RESULT_QUEUE_NAME,
                body=result_body)
            return True
        except Exception as e:
            print("An error occured operation will stop. See details:")
            print(e)
            return False

    def get_client(self) -> BlockingConnection:
        return self.client

    def get_channel(self) -> BlockingChannel:
        return self.channel
    
    def get_request_queue_name(self) -> str:
        return REQUEST_QUEUE_NAME

    def get_result_queue_name(self) -> str:
        return RESULT_QUEUE_NAME

if __name__ == "__main__":
    pass