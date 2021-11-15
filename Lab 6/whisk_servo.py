import paho.mqtt.client as mqtt
import uuid
import time
from adafruit_servokit import ServoKit
# the # wildcard means we subscribe to all subtopics of IDD
topic = 'IDD/whisk'

kit = ServoKit(channels=16)

servo = kit.servo[2]

servo.set_pulse_width_range(500,2500)


# some other examples
# topic = 'IDD/a/fun/topic'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
	#print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
        angle = msg.payload.decode('UTF-8')
        angle = int(angle)
        print(angle)
        servo.angle = angle
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing


# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop
client.loop_forever()
