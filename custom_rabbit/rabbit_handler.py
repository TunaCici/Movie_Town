import pika
import json
import time
import threading

from pika.adapters.blocking_connection import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from pika.spec import Basic
from pika.spec import BasicProperties

# connection and authentication info
HOST = "localhost"
PORT = 5672
USERNAME = "tunac"
PASSWORD = "123456"
AUTH = pika.PlainCredentials(
    USERNAME, PASSWORD, erase_on_connect=True)
CONNECTION_PARAMS = pika.ConnectionParameters(
    host=HOST, port=PORT, credentials=AUTH)

# database releated info
REQUEST_QUEUE_NAME = "request_queue"
RESULT_QUEUE_NAME = "result_queue"

# general info
MAX_RECONNECT_COUNT = 30 # times

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
    client: BlockingConnection = None

    channel: BlockingChannel = None
    channel_number: int = -1

    def __init__(self):
        print("Starting a new RabbitMQ client.")
        print(f"Host: {HOST}, Port: {PORT}")
        try:
            self.client = BlockingConnection(CONNECTION_PARAMS)
        except Exception as e:
            print("An error occured when connecting to RabbitMQ.")
            return None
        
        # intialize channel
        self.channel = self.client.channel()
        self.channel_number= self.channel.channel_number

        # initialize queues
        self.channel.queue_declare(REQUEST_QUEUE_NAME)
        self.channel.queue_declare(RESULT_QUEUE_NAME)
        
        self.is_running = True

    def running(self) -> bool:
        # check if client or channel exists
        if self.client is None or self.channel is None:
            print("No client or channel exists.")
            return False

        # send a heartbeat
        try:
            self.client.sleep(0.001)
        except:
            pass

        # check if channel is open
        if self.channel.is_open:
            print("Channel is open")
            return True
        
        # no active connection found
        print("Connection dropped.")
        i = 1
        while i <= MAX_RECONNECT_COUNT:
            print(f"Trying to reconnect [{i}/{MAX_RECONNECT_COUNT}]")
            try:
                self.client = BlockingConnection(CONNECTION_PARAMS)
                print("Successfully reconnected.")
                return True
            except Exception as e:
                i += 1
                time.sleep(1)
                
        return False

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
    print("Creating an instance of RabbitMQ handler.")
    inst = RabbitHandler()

    if not inst.running():
        print("Failed to create an instance. Exiting.")
        exit(-1)
    
    while True:
        print("***********************")
        print("1. Check connection")
        print("2. Get channel no")
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
            no = inst.get_channel_number()
            print(no)
        else:
            print("Invalid operation, try again.")