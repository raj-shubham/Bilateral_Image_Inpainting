import json
import os
import sys

CONFIG_FILE_PATH = os.path.dirname(__file__)
CONFIG_FILE_NAME = "settings.config"

def open_config_file(config_file_path=None, config_file_name=None):
	if None == config_file_path:
		config_file_path = CONFIG_FILE_PATH
	if None == config_file_name:
		config_file_name = CONFIG_FILE_NAME
	absolute_file_path = os.path.join(config_file_path, config_file_name)
	# check if file exists
	file_exists = os.path.exists(absolute_file_path)
	if not file_exists:
		return -1
	config_json = None
	with open(absolute_file_path) as config_file:
		config_json = json.load(config_file)
	return config_json

