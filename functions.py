import configparser
import logging
import os
import shutil


def load_config():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    ini_filename = "config.ini"

    if not os.path.isfile(os.path.join(root_dir, ini_filename)):
        shutil.copy(os.path.join(root_dir, "ini_template"), os.path.join(root_dir, ini_filename))

    config = configparser.ConfigParser()
    config.read(os.path.join(root_dir, "config.ini"))

    if 'lastfm' not in config or 'mysql' not in config:
        raise ValueError("Invalid {0} config file".format(ini_filename))
    if not config['lastfm'].get('api_key') or not config['lastfm'].get('shared_secret'):
        logging.getLogger(__name__).error("Add your lastfm API key and shared secret into {0}".format(ini_filename))
        exit(1)

    for x in ['host', 'username', 'db']:
        if not config['mysql'].get(x):
            logging.getLogger(__name__).error("Add your mysql server details into {0}".format(ini_filename))
            exit(1)

    return config