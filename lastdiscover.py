#!/usr/bin/env python3
import urllib3
import sqlite3
import json

http = urllib3.PoolManager()

page = 1
parsed_data = []

while True:
	r = http.request('GET', 'http://ws.audioscrobbler.com/2.0/', fields={'api_key': '55c3d9442dc812969a1925cfdc85a7bc', 'format': 'json', 'method': 'user.getrecenttracks', 'user': 'konzertheld', 'limit': 200, 'page': page})
	jsondata = json.loads(r.data.decode('utf-8'))

	for track in jsondata["recenttracks"]["track"]:
		if "@attr" in track and "nowplaying" in track["@attr"] and track["@attr"]["nowplaying"] == "true":
			continue
		parsed_data.append((track["artist"]["#text"], track["artist"]["mbid"], track["name"], track["mbid"], track["date"]["uts"]))

	page = page + 1
	print("Loaded page " + jsondata["recenttracks"]["@attr"]["page"])
	if jsondata["recenttracks"]["@attr"]["page"] == jsondata["recenttracks"]["@attr"]["totalPages"]:
		break

conn = sqlite3.connect('recenttracks.db')
c = conn.cursor()
c.execute("DELETE FROM recenttracks")
c.executemany('INSERT INTO recenttracks (artist, artist_mbid, title, title_mbid, time) VALUES (?,?,?,?,?)', parsed_data)
conn.commit()
conn.close()