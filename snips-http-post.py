#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import spotifywebapi
import requests

HOST = '192.169.0.250'
HOST_SERVER_EWEN = 'http://192.169.0.231:8000/bot'
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    # subscribe to the playback events
    client.subscribe('hermes/intent/#')
    # subscribe to hotwords (hey snips)
    client.subscribe("hermes/hotword/default/detected")

def on_message(client, userdata, msg):
    print("Message received on topic {0}: {1}"\
        .format(msg.topic, msg.payload))
    payload = json.loads(msg.payload)
    slots = payload["slots"]
    slots_dict = dict(slots[0])
    slot_name = slots_dict["slotName"]

    # the hotword
    if msg.topic == 'hermes/hotword/default/detected':
        print("hotword detected")
        spotifywebapi.pause_track()

    # spotify intent
    elif msg.topic == 'hermes/intent/zoug:playbackControl':
        print("playback intent")
        if len(slots) == 1:
            if slot_name == "pauseTrack":
                print("Pause track")
                spotifywebapi.pause_track()
            elif slot_name == "playTrack":
                print("Play track")
                spotifywebapi.play_track()
            elif slot_name == "nextTrack":
                print("Next track")
                spotifywebapi.next_track()
            elif slot_name == "previousTrack":
                print("Previous track")
                spotifywebapi.prev_track()
            elif slot_name == "mediumVolume":
                print("Medium volume")
                spotifywebapi.medium_volume()
            elif slot_name == "lowVolume":
                print("Low volume")
                spotifywebapi.low_volume()
            elif slot_name == "highVolume":
                print("High volume")
                spotifywebapi.high_volume()
            else:
                print("Unknown slot name: {}".format(slot_name))
        else:
            print("More than one slot detected, dropping")

    # motor intent
    else:
        print("motor intent of length {}".format(len(slots)))
        if len(slots) == 1:
            if slot_name == "stopMotors":
                print("stopping motors")
                r = requests.post(HOST_SERVER_EWEN, data='stop')
                print(r.status_code)
            else:
                print("starting motors")
                r = requests.post(HOST_SERVER_EWEN, data='start')
                print(r.status_code)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, PORT, 60)
    client.loop_forever()
