#!/usr/bin/env python

# Copyright (C) 2013 Guillaume Seguin <guillaume@segu.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import json
try:
    from http.client import HTTPSConnection
except ImportError:  # python2
    from httplib import HTTPSConnection
import sys

deezer_api = "/2.0/"
connection = HTTPSConnection("api.deezer.com")

def get_data(url):
    connection.request("GET", url)
    response = connection.getresponse()
    return json.loads(response.read().decode("utf-8"))

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
        print("  Playlist %s" % playlist["title"])
        for track in playlist["tracks"]["data"]:
            print("    %s -- by %s" % (track["title"], track["artist"]["name"]))
