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
import argparse

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
    parser = argparse.ArgumentParser(description = 'Deezer export script')
    parser.add_argument('uid', type = int, help = "User identifier")
    parser.add_argument('-j', '--json', '--export', dest = "export",
                        help = "Export playlists in a simple json format"
                               "to the specified file")
    args = parser.parse_args()
    userdata = get_user_info(args.uid)
    print("Playlists for user %s" % userdata["name"])
    playlists = get_user_playlists(args.uid)
    playlists_data = []
    for row in playlists["data"]:
        playlistid = row["id"]
        playlist = get_playlist(playlistid)
        playlists_data.append(playlist)
        print("  Playlist %s" % playlist["title"])
        for track in playlist["tracks"]["data"]:
            print("    %s -- by %s" % (track["title"], track["artist"]["name"]))
    if args.export is not None:
        data = {"uid": args.uid, "user": userdata["name"], "playlists": []}
        for playlist in playlists_data:
            tracks = [{"title": track["title"],
                       "artist": track["artist"]["name"],
                       "album": track["album"]["title"]}
                      for track in playlist["tracks"]["data"]]
            cur_playlist = {"title": playlist["title"], "tracks": tracks}
            data["playlists"].append(cur_playlist)
        with open(args.export, "w") as f:
            json.dump(data, f)
