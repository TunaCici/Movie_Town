"""
Author: Tuna Cici
Created: 19/08/2021
"""

import os
import inspect
import logging
import logging.handlers


if __name__ == "utils." + os.path.basename(__file__)[:-3]:
    # importing from outside the package
    from utils import config
else:
    # importing from main and inside the package
    import config

class CustomLogger:
    #class member(s)
    logger = None

    #init
    def __init__(self):
        #get the callers filename
        filename = inspect.stack()[1].filename
        filename = os.path.basename(filename)
        #get the root logger
        rootlogger = logging.getLogger()
        #set overall level to debug, default is warning for root logger
        rootlogger.setLevel(logging.DEBUG)

        #set log format
        formatter = logging.Formatter(config.LOG_FORMAT)

        #setup logging to file, rotating every minute
        filelog = logging.handlers.TimedRotatingFileHandler(config.LOG_FILE_DIR,
                        when='m', interval=1, encoding="utf-8")
        filelog.setLevel(logging.DEBUG)
        filelog.setFormatter(formatter)
        filelog.namer = lambda name: name.replace(".txt", "") + ".txt"
        rootlogger.addHandler(filelog)

        #setup logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        rootlogger.addHandler(console)

        #get a logger for my script
        self.logger = logging.getLogger(filename)

    def log_info(self, text : str):
        """
        Logs the given text to both console and logfile.
        Level: INFO
        """
        self.logger.info(text)
    
    def log_warning(self, text : str):
        """
        Logs the given text to both console and logfile
        Level: WARNING
        """
        self.logger.warning(text)

    def log_error(self, text : str):
        """
        Logs the given text to both console and logfile
        Level: ERROR
        """
        self.logger.error(text)
        print("An error occured. See the above log. Exiting program...")
        exit(-1)