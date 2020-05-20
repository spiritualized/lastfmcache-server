from collections import OrderedDict

import jsonpickle as jsonpickle
from flask import Blueprint
from injector import inject

from lastfmcache import LastfmCache

api_v1 = Blueprint('api', __name__)


@inject
@api_v1.route('/artists/<artist>')
def get_artist(lastfmcache: LastfmCache, artist: str):
    artist = LastfmCache.api_urldecode(artist)
    try:
        return jsonpickle.encode(lastfmcache.get_artist(artist), unpicklable=False)
    except LastfmCache.ArtistNotFoundError:
        return "Artist not found: '{0}'".format(artist), 404

@inject
@api_v1.route('/artists/<artist>/releases/<release>')
def get_release(lastfmcache: LastfmCache, artist: str, release: str):
    artist = LastfmCache.api_urldecode(artist)
    release = LastfmCache.api_urldecode(release)
    try:
        return jsonpickle.encode(lastfmcache.get_release(artist, release), unpicklable=False)
    except LastfmCache.ReleaseNotFoundError:
        return "Release not found: '{0}' by '{1}'".format(artist, release), 404
