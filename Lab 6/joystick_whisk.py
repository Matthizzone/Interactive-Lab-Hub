import time
import board
import busio
import adafruit_mpr121

import qwiic_joystick

import paho.mqtt.client as mqtt
import uuid

import math

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/whisk'

i2c = busio.I2C(board.SCL, board.SDA)

#mpr121 = adafruit_mpr121.MPR121(i2c)

print("\nSparkFun qwiic Joystick   Example 1\n")
myJoystick = qwiic_joystick.QwiicJoystick()

if myJoystick.connected == False:
    print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    exit(0)

myJoystick.begin()

print("Initialized. Firmware Version: %s" % myJoystick.version)




while True:
    #msg = ("X: %d, Y: %d, Button: %d" % ( \
    #            myJoystick.horizontal, \
    #            myJoystick.vertical, \
    #            myJoystick.button))
    x = myJoystick.horizontal / 512.0 - 1.0
    y = myJoystick.vertical / 512.0 - 1.0
    msg = int(math.atan(y/x) / math.pi * 180 + 90)
    client.publish(topic, msg)
    '''
    for i in range(12):
        if mpr121[i].value:
            val = f"Twizzler {i} touched!"
            print(val)
            client.publish(topic, val)
    '''
    time.sleep(0.25)
