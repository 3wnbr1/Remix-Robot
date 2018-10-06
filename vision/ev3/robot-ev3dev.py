#!/usr/bin/python3

# https://github.com/ev3dev/ev3dev-lang-python
# 

import requests
import json
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
import time
import argparse

SERVER_URL="http://192.169.0.231:8000/results"


td=MoveTank(OUTPUT_A,OUTPUT_B)

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
    print("SRV>%s" % fulldata)
    traiteOneData(fulldata)
    
def traiteOneData( fulldata ):
    if fulldata[0]=='[':
        try:
            data=json.loads(fulldata)
        except:
            return "invalid JSON returned"
    else:
        data=[eval(fulldata)]
    
    for one in data:
        motorA=int(100 * one[0] / 255)
        motorB=int(100 * one[1] / 255)
        duration=one[2]
        
        if duration>0:
            print("MTR> A(%d) B(%d) %d" % (motorA, motorB, duration))
            td.on_for_seconds(SpeedPercent(motorA), SpeedPercent(motorB), duration)
        
    return ""

traiteOneData('[0,0,0]')
print("Verify the ev3dev motor interface is answering")
traiteOneData('10,10,1')
traiteOneData('-10,-10,1')

traiteOneData('[[10,10,1],[-10,-10,1]]')


while True:
    ret=traiteOne()
    if len(ret)>0:
        print( "ERR> %s" % ret)
    time.sleep(0.5)