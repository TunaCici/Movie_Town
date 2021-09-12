import json

from utils import logger
from utils import handler
from utils import config
from utils import feature_pack

from custom_rabbit import rabbit_handler

from custom_mongo import mongo_handler
from custom_elastic import elastic_handler

from pika.adapters.blocking_connection import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from pika.spec import Basic
from pika.spec import BasicProperties

WORKER_LOGGER = logger.CustomLogger()

MONGO_CLIENT: mongo_handler.MongoHandler
ELASTIC_CLIENT: elastic_handler.ElasticHandler
RABBIT_CLIENT: rabbit_handler.RabbitHandler

# establish rabbitmq connection
WORKER_LOGGER.log_info("Connecting to DBs.")
try:
    MONGO_CLIENT = mongo_handler.MongoHandler()
except Exception as e:
    WORKER_LOGGER.log_error(f"Connection failed to MongoDB.\n\t{e}")
try:
    ELASTIC_CLIENT = elastic_handler.ElasticHandler()
except Exception as e:
    WORKER_LOGGER.log_error(f"Connection failed to ElasticSearch.\n\t{e}") 
try:
    RABBIT_CLIENT = rabbit_handler.RabbitHandler()
except Exception as e:
    WORKER_LOGGER.log_error(f"Connection failed to RabbitMQ.\n\t{e}") 

WORKER_LOGGER.log_info("Connection successful to DBs.")

def callback(
    ch : BlockingChannel,
    method : Basic.Deliver,
    properties : BasicProperties,
    body : bytes):
    WORKER_LOGGER.log_info(f"Retriving new requst from user")
    # convert bytes to python dict type
    dict_body : dict = json.loads(body.decode("UTF-8"))
    WORKER_LOGGER.log_info(f"Request made by: {dict_body.get('owner')}")
    print(dict_body)

    # result struct
    result = {
        "owner": dict_body.get("owner"),
        "operation": None,
        "result": None,
        "data": None,
        "extras": None
    }

    # decide on the operation
    operation = dict_body.get("operation", None)
    result.update({"operation": operation})

    if operation == "get_user":
        WORKER_LOGGER.log_info("Getting user.")
        username = dict_body.get("data")
        ret_value = handler.get_user(MONGO_CLIENT, username)
        ret_value.pop("_id")
        if ret_value:
            result.update({"result": "success"})
            result.update({"data": json.dumps(ret_value)})
            WORKER_LOGGER.log_info("Successfully got the user.")
        else:
            result.update({"result": "fail"})
            WORKER_LOGGER.log_warning("Failed to get user.")

    elif operation == "handle_login":
        WORKER_LOGGER.log_info("Validating login form.")
        form = dict_body.get("data")
        form = json.loads(form)
        ret_value = handler.handle_login(MONGO_CLIENT, form)
        if ret_value == "success":
            result.update({"result": ret_value})
            WORKER_LOGGER.log_info("Validation login form successful.")
        else:
            result.update({"result": "fail"})
            result.update({"data": ret_value})
            WORKER_LOGGER.log_warning("Failed to validate login form.")

    elif operation == "handle_signup":
        WORKER_LOGGER.log_info("Validating signup form.")
        form = dict_body.get("data")
        form = json.loads(form)
        ret_value = handler.handle_signup(MONGO_CLIENT, form)
        print("after")
        if ret_value == "success":
            result.update({"result": ret_value})
            WORKER_LOGGER.log_info("Validation signup form successful.")
        else:
            result.update({"result": "fail"})
            result.update({"data": ret_value})
            WORKER_LOGGER.log_warning("Failed to validate signup form.")

    elif operation == "handle_search":
        WORKER_LOGGER.log_info("Searching through ElasticSearch.")
        search_str = dict_body.get("data")
        WORKER_LOGGER.log_info(f"Keyword: {search_str}")
        ret_value = handler.handle_search(ELASTIC_CLIENT, search_str)
        if ret_value:
            result.update({"result": "success"})
            WORKER_LOGGER.log_info(
                f"Searching successful Found '{len(ret_value)}' results.")
            result.update({"data": json.dumps(ret_value)})
        else:
            result.update({"result": "fail"})
            result.update({"data": []})
            WORKER_LOGGER.log_warning("Failed to search.")

    elif operation == "handle_password_change":
        WORKER_LOGGER.log_info("Changing password.")
        pair = dict_body.get("data")
        pair = json.loads(pair
        )
        user = pair.get("user")
        
        form = pair.get("form")

        ret_value = handler.handle_password_change(
            MONGO_CLIENT, user, form)
        if ret_value == "success":
            result.update({"result": "success"})
            WORKER_LOGGER.log_info("Successfully changed the password.")
        else:
            result.update({"result": "fail"})
            WORKER_LOGGER.log_warning("Failed to change the password.")

    elif operation == "handle_watchlist_add":
        WORKER_LOGGER.log_info("Adding movie to the watchlist.")
        movie = dict_body.get("data")
        WORKER_LOGGER.log_info(f"Movies is: {movie}")
        id = dict_body.get("owner")
        ret_value = handler.handle_watchlist_add(
            MONGO_CLIENT, id, movie)
        if ret_value == "success":
            result.update({"result": "success"})
            WORKER_LOGGER.log_info("Successfully added movie to the watchlist.")
        else:
            result.update({"result": "fail"})
            WORKER_LOGGER.log_warning("Failed to add movie to the watchlist.")

    elif operation == "handle_watchlist_remove":
        WORKER_LOGGER.log_info("Removing movie from the watchlist.")
        movie = dict_body.get("data")
        WORKER_LOGGER.log_info(f"Movies is: {movie}")
        id = dict_body.get("owner")
        ret_value = handler.handle_watchlist_remove(
            MONGO_CLIENT, id, movie)
        if ret_value == "success":
            result.update({"result": "success"})
            WORKER_LOGGER.log_info("Successfully removed the movie to the watchlist.")
        else:
            result.update({"result": "fail"})
            WORKER_LOGGER.log_warning("Failed to removed the movie to the watchlist.")

    elif operation == "check_integrity":
        WORKER_LOGGER.log_info("Checking integrity.")
        pair = dict_body.get("data")
        pair = json.loads(pair)
        start = pair.get("start")
        end = pair.get("end")
        WORKER_LOGGER.log_info(f"Start: {start}\tEnd: {end}")
        ret_value = handler.check_integrity(
            MONGO_CLIENT, ELASTIC_CLIENT, start, end)
        if ret_value == True:
            result.update({"result": "success"})
            WORKER_LOGGER.log_info("Successfully checked integrity.")
        else:
            result.update({"result": "fail"})
            WORKER_LOGGER.log_warning("Failed to chek integrity.")
    else:
        WORKER_LOGGER.log_warning(f"Invalid operation: {operation}")

    RABBIT_CLIENT.result_add(
        result.get("owner"),
        result.get("operation"),
        result.get("result"),
        result.get("data"),
        result.get("extras")
    )

if __name__ == "__main__":
    WORKER_LOGGER.log_info("Worker started.")
    
    # prepare to consume
    worker_client = rabbit_handler.RabbitHandler()
    worker_channel = worker_client.get_channel()
    worker_channel_name = worker_client.get_request_queue_name()

    # start consming
    worker_channel.basic_consume(
        queue=worker_channel_name,
        on_message_callback=callback,
        auto_ack=True
    )

    try:
        worker_channel.start_consuming()
    except KeyboardInterrupt as e:
        WORKER_LOGGER.log_warning("Detecting keyboard interrupt. Exiting the program.")
        exit(0)
    except Exception as e:
        WORKER_LOGGER.log_error(f"Something went wrong. See the details.\t\n{e}")
        exit(-1)