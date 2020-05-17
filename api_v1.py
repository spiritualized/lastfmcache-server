from collections import OrderedDict

import jsonpickle as jsonpickle
from flask import Blueprint
from injector import inject

from lastfmcache import LastfmCache

api_v1 = Blueprint('api', __name__)


@inject
@api_v1.route('/artists/<artist>')
def get_artist(lastfmcache: LastfmCache, artist: str):
    artist = artist.replace('∕', '/')
    try:
        artist_obj = lastfmcache.get_artist(artist)
        return jsonpickle.encode(artist_obj, unpicklable=False)
    except LastfmCache.ArtistNotFoundError:
        return "Artist not found: '{0}'".format(artist), 404

@inject
@api_v1.route('/artists/<artist>/releases/<release>')
def get_release(lastfmcache: LastfmCache, artist: str, release: str):
    artist = artist.replace('∕', '/')
    release = release.replace('∕', '/')
    try:
        release_obj = lastfmcache.get_release(artist, release)
        return jsonpickle.encode(release_obj, unpicklable=False)
    except LastfmCache.ReleaseNotFoundError:
        return "Release not found: '{0}' by '{1}'".format(artist, release), 404
