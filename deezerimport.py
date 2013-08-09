#!/usr/bin/env python

import json
try:
    from urllib.request import urlopen
except ImportError:  # python2
    from urllib2 import urlopen
import sys

deezer_api = "https://api.deezer.com/2.0/"

def get_data(url):
    req = urlopen(url)
    try:
        encoding = req.headers.get_content_charset()
        return json.loads(req.read().decode(encoding))
    except AttributeError:  # python2
        return json.load(urlopen(url))

def get_user_info(userid):
    url = deezer_api + "user/%d" % userid
    return get_data(url)

def get_user_playlists(userid):
    url = deezer_api + "user/%d/playlists" % userid
    return get_data(url)

def get_playlist(playlistid):
    url = deezer_api + "playlist/%d" % playlistid
    return get_data(url)

if __name__ == "__main__":
    uid = int(sys.argv[1])
    userdata = get_user_info(uid)
    print("Playlists for user %s" % userdata["name"])
    playlists = get_user_playlists(uid)
    for row in playlists["data"]:
        playlistid = row["id"]
        playlist = get_playlist(playlistid)
        print "  Playlist %s" % playlist["title"]
        for track in playlist["tracks"]["data"]:
            print "    %s -- by %s" % (track["title"], track["artist"]["name"])
