import os
import configparser

SETTINGS_FILE_NAME = "fids.cfg"

config = configparser.ConfigParser()
config.read_dict({"topsecret.server.com": {"Port": 21212}})

def _read_config():
    config.read(SETTINGS_FILE_NAME)
    

def read_config():
    if not os.path.isfile(SETTINGS_FILE_NAME):
        with open(SETTINGS_FILE_NAME, "w") as f:
            config.write(f)
    _read_config()