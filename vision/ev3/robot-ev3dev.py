#!/usr/bin/python3

# https://github.com/ev3dev/ev3dev-lang-python
#

import requests
import json
import time
import argparse
import math
import sys

SERVER_URL="http://192.169.0.231:8000/results"

TRAITE_EACH=1.0
WHEEL_RADIUS=0.05  # Robot EV3 Wheel radius
WHEEL_PERIMETER = 2 * math.pi * WHEEL_RADIUS
DISTANCE_TO_KEEP = 2
ROTATION_MAX = 3

INVERTED = 1

SPEED_MOTOR = 10 # 0..100 % 100=full speed

def traiteOne():
    """
    return '' on success
           'Reason of failure'
    """
    try:
        rq=requests.get(SERVER_URL)
    except:
        return "Unable to connect the server"
    if rq.status_code!=200:
        return "web server return status: %s" % rq.status_code
    fulldata=rq.text
    if fulldata[0:2]!='[[' and fulldata[0]=='[':
        fulldata='['+fulldata+']'
    traiteOneData(fulldata)

def traiteOneData( fulldata ):
    """
    splitted into 2: server vs motor comm

    param: fulldata: string returned by the server, if starts with a [ then interpreted as a JSON string

    data provided by the server (calculated from camera image capture)
    distance-to-user, shift-from-center, 0|1        distance in meter and status 0 (stop, do nothing, stay still)
    """
    print("SRV>%s" % fulldata)
    if fulldata[0]=='[':
        try:
            data=json.loads(fulldata)
        except:
            return "invalid JSON returned"
    else:
        data=[eval(fulldata)]

    for one in data:
        status = one[2]
        if status==0:
            print("MTR> invalidated measure")
        else:
            distance_to_object = one[1]
            shift = INVERTED * one[0]
            move = math.sqrt( ( distance_to_object - DISTANCE_TO_KEEP ) ** 2 + shift ** 2 )
            rotation = move / WHEEL_PERIMETER
            if rotation>ROTATION_MAX:
                rotation=ROTATION_MAX
            if shift < 0:
                # turn left
                if move != 0:
                    motorA = 1 - (-shift)/distance_to_object
                    motorB = 1
                else:
                    motorA = 0
                    motorB = 0
            else:
                # turn right
                if move != 0:
                    motorA = 1
                    motorB = 1 - (shift)/distance_to_object
                else:
                    motorA = 0
                    motorB = 1

            direction=-1
            if rotation<0:
                direction=1
                rotation=-rotation

            A = motorA * SPEED_MOTOR * direction
            B = motorB * SPEED_MOTOR * direction
            print("MTR> A(%.2f) B(%.2f) %.0f" % (A, B, rotation))
            if not TEST_OFFLINE:
                td.on_for_rotations(SpeedPercent(A), SpeedPercent(B), rotation)

    return ""


parser = argparse.ArgumentParser(description='robot-ev3')
parser.add_argument('--speed', type=int, default=10,
                    help='percentage of speed engine')
parser.add_argument('--distance', type=int, default=2,
                    help='Minimal distance in meter to keep to object')
parser.add_argument('--test', default=0, action="store_true",
                    help='Enable test mode')
parser.add_argument('--rotation', default=3, type=int,
                    help='Maximum acceptable rotation')
parser.add_argument('--inverted', default=1, action="store_true",
                    help='Invert left/right')


args = parser.parse_args()

SPEED_MOTOR = args.speed
DISTANCE_TO_KEEP = args.distance
ROTATION_MAX = args.rotation
INVERTED = 1
if args.inverted:
    INVERTED = -1

TEST_OFFLINE = args.test

if not TEST_OFFLINE:
    from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
    td=MoveTank(OUTPUT_A,OUTPUT_B)


print("Distance to keep to object: %.1f m" % DISTANCE_TO_KEEP)
print("Wheel perimeter: %.2f m" % WHEEL_PERIMETER)
print("Maximum rotation: %d" % ROTATION_MAX)

if TEST_OFFLINE:
    print("Verify the ev3dev motor interface is answering")
    traiteOneData('4,0,1')
    traiteOneData('3.5,0,1')

    traiteOneData('[[1.5,0,1],[2,-0.5,1],[2,0,1],[2,0.5,1]]')
    sys.exit(0)

while True:
    curtime=time.time()
    ret=traiteOne()
    if ret and len(ret)>0:
        print( "%s-ERR> %s" % (time.strftime('%H:%M:%S'), ret) )

    time2next=time.time()-curtime
    if time2next<TRAITE_EACH:
        time.sleep(TRAITE_EACH-time2next)
