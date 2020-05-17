import sys
from configparser import ConfigParser

from flask import Flask
from flask_injector import FlaskInjector
from injector import singleton, inject

from api_v1 import api_v1
from functions import load_config
from lastfmcache import LastfmCache


@inject
def init_lastfmcache(config: ConfigParser):
    lastfmcache = LastfmCache(config['lastfm']['api_key'], config['lastfm']['shared_secret'])
    lastfmcache.enable_mysql_cache(config['mysql']['host'], config['mysql']['username'],
                                   config['mysql']['password'], config['mysql']['db'])
    return lastfmcache

def configure(binder):
    binder.bind(ConfigParser, to=load_config, scope=singleton)
    binder.bind(LastfmCache, to=init_lastfmcache, scope=singleton)

def main():
    app = Flask(__name__)
    app.register_blueprint(api_v1, url_prefix='/lastfmcache/api/v1')

    FlaskInjector(app=app, modules=[configure])

    app.run()

def init():
    if __name__ == "__main__":
        sys.exit(main())

init()
