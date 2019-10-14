import logging 
import sys
import os 

"""
LOG LEVELS : When set to a value ignores all message levels below it.

CRITICAL: 50
ERROR: 40
WARNING: 30
INFO: 20
DEBUG: 10
NOTSET: 0

"""
from config import config

config_json = config.open_config_file()

LOG_FILE_DIRECTORY = config_json["syslog"]["log_directory"]
LOG_FILE_NAME = config_json["syslog"]["log_file"]
LOG_ABSOLUTE_PATH = os.path.join(LOG_FILE_DIRECTORY, LOG_FILE_NAME)

LOG_MESSAGE_FORMAT = config_json["syslog"]["log_message_format"]

LOG_FILE_MODE = config_json["syslog"]["log_file_mode"]

LOG_LEVEL = config_json["syslog"]["log_level"]

if not os.path.exists(LOG_ABSOLUTE_PATH):
	open(LOG_ABSOLUTE_PATH, 'a').close()

logging.basicConfig(filename=LOG_ABSOLUTE_PATH, format=LOG_MESSAGE_FORMAT,\
                    filemode=LOG_FILE_MODE)

logger=logging.getLogger() 

logger.setLevel(LOG_LEVEL)

def debug(message):
	logger.debug(message)

def info(message):
	logger.info(message)

def warning(message):
	logger.warning(message)

def error(message):
	logger.error(message)

def critical(message):
	logger.critical(message)