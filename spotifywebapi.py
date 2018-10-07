#!/usr/bin/env python
import spotipy
import spotipy.util
import time
import json
import requests

def spotify_object():
    # we use spotipy just to obtain a token, saved in .chache-<username>
    scope = "user-modify-playback-state"
    token = spotipy.util.prompt_for_user_token("yzoug",scope,client_id='b1bc4617fd684949b05d429b0c002791',client_secret='7d39fefe3f614c61b7b52fbb3eb3b3b3',redirect_uri='https://example.com/callback')
    sp = spotipy.client.Spotify(auth=token)
    sp.trace = True
    sp.trace_out = True
    return sp

def get_token_if_valid():
    epoch_now = time.time()
    print("Current epoch: " + str(epoch_now))
    with open('.cache-yzoug') as json_token:
        d = json.load(json_token)
    eol_token = d["expires_at"]
    print("Token expires at: " + str(eol_token))
    if epoch_now > eol_token:
        print("Token expired")
        return None
    else:
        return d["access_token"]

def create_request_headers():
    # exemple: headers {'Content-Type': 'application/json', 'Authorization': 'Bearer BQDePkg5q9py-mXPhZB4ZOwFHN8w2UIOfLdFL13xbVRyhMY72tLBVYAhGtsad8VOwc4BoBJAfH3W3D6x3c6cZb3fYkdmVJpp9-mjCkaK7ej9pnaHJONc7aQO-qeynPHs-NqVSquVVPZZ1joNELkRF1nVa5Zl'}
    headers = dict()
    headers['Content-Type'] = 'application/json'
    token = get_token_if_valid()
    print("Token for headers: " + token)
    if token == None:
        print("Headers not created")
        return None
    else:
        headers['Authorization'] = 'Bearer ' + token
        return headers

def next_track():
    sp = spotify_object()
    headers = create_request_headers()
    r = requests.post("https://api.spotify.com/v1/me/player/next", headers=headers)
    return r.status_code

def prev_track():
    sp = spotify_object()
    headers = create_request_headers()
    r = requests.post("https://api.spotify.com/v1/me/player/previous", headers=headers)
    return r.status_code

def pause_track():
    sp = spotify_object()
    headers = create_request_headers()
    r = requests.put("https://api.spotify.com/v1/me/player/pause", headers=headers)
    return r.status_code

def play_track():
    sp = spotify_object()
    headers = create_request_headers()
    r = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers)
    return r.status_code

def low_volume():
    sp = spotify_object()
    headers = create_request_headers()
    r = requests.put("https://api.spotify.com/v1/me/player/volume?volume_percent=20", headers=headers)
    return r.status_code

def high_volume():
    sp = spotify_object()
    headers = create_request_headers()
    r = requests.put("https://api.spotify.com/v1/me/player/volume?volume_percent=100", headers=headers)
    return r.status_code

def medium_volume():
    sp = spotify_object()
    headers = create_request_headers()
    r = requests.put("https://api.spotify.com/v1/me/player/volume?volume_percent=50", headers=headers)
    return r.status_code

if __name__ == "__main__":
    # handles asking for the token
    sp = spotify_object()

    # create headers
    headers = create_request_headers()
    print(headers)

    # next song
    next_track()

    time.sleep(3)

    # previous song
    prev_track()

    time.sleep(3)

    # pause playback
    pause_track()

    time.sleep(3)

    # start playback
    play_track()
