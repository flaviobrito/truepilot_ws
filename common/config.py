import json
from json import JSONDecodeError
import logging
from pathlib import Path

# the logging level needs to be set, at least for logging.info so that info messages
# can appear on the terminal.
##
logging.basicConfig(level=logging.INFO)
"""
TODO - create a function that reads a config from json file then
        print the content of the settings
steps: 
- import json module
- import patlib module
- import logging module
- define logging level
- define global variables
- create a function the receives a file path
- create a variable that receives the content of json file
- return the settings
- call the function passing the path of the configuration file
"""

## Global 

BASE_PATH = Path(__file__).parent.parent
CONFIG_FILE = BASE_PATH / "config" / "settings.json"


def get_config(path):
    try:
        with open(path, "r") as json_file:
            config = json.load(json_file)
        return config
    except (FileNotFoundError, JSONDecodeError) as e:
        logging.error(f"Error trying to read config settings \n{e}")



settings = get_config(CONFIG_FILE)