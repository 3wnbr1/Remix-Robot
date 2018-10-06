#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import spotifywebapi

HOST = '192.169.0.250'
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    # subscribe to the playback events
    client.subscribe('hermes/intent/#')

# we only have one intent, so we only care about the slots
def on_message(client, userdata, msg):
    print("Message received on topic {0}: {1}"\
        .format(msg.topic, msg.payload))
    payload = json.loads(msg.payload)
    print("Payload: " + str(payload))
    # Payload: {'sessionId': '3128ac87-ca00-4ad7-9e9b-1b101e3048db', 'customData': None, 'siteId': 'default', 'input': 'go', 'intent': {'intentName': 'zoug:playbackControl', 'probability': 1.0}, 'slots': [{'rawValue': 'go', 'value': {'kind': 'Custom', 'value': 'go'}, 'range': {'start': 0, 'end': 2}, 'entity': 'snips/default--playTrack', 'slotName': 'playTrack'}]}
    slots = payload["slots"]
    slots_dict = dict(slots[0])
    slot_name = slots_dict["slotName"]
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
        else:
            print("Previous track")
            spotifywebapi.prev_track()
    else:
        print("More than one intent detected, dropping")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, PORT, 60)
    client.loop_forever()
