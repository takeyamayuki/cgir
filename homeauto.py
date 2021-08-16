#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import subprocess
import json
import os

HOST = 'mqtt.beebotte.com'
PORT = 8883
CA_CERTS = 'mqtt.beebotte.com.pem'
TOKEN = 'XXXXXXXXXXXXXXXXXXXXXX'        #Beebotteで作成したチャンネルのトークンを入力
TOPIC = 'raspberrypi/SmartRemocon'      #Beebotteで作成したトピック名を入力
i = 0                                   #0:エアコン止まっている状態 1:エアコン動いている状態


def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))

def on_disconnect(client, userdata, flags, respons_code):
    print("Unexpected disconnection.")
    client.loop_stop()

def on_message(client, userdata, msg):
    global i
    print(msg.topic + ' ' + str(msg.payload))
    data = json.loads(msg.payload.decode("utf-8"))["data"][0]
    print(msg.payload.decode("utf-8"))
    print(data)

    if (data["room"] == 'living'):
        # control aricon
        if (data["device"] == 'aircon'):
            if   (data["action"] == 'on'):
                if (i==0):
                    #os.chdir('/home/pi/Desktop/cgir-master')
                    subprocess.run(['./cgirtool.py', 'send', 'aircon_power'])
                    i=1 #エアコンを動いている状態にする
                elif (i==1):
                    #os.chdir('/home/pi/Desktop/cgir-master')
                    subprocess.run(['./cgirtool.py', 'send', 'aircon_stop'])
                    i=0 #エアコンを止まっている状態にする

        # control light
        elif (data["device"] == 'light'):
            if (data["action"] == 'on'):
                os.chdir('/home/pi/Desktop/cgir-master')
                subprocess.run(['./cgirtool.py', 'send', 'light_power'])

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set('token:%s' % TOKEN)
    client.tls_set(CA_CERTS)
    client.connect(HOST, PORT)
    client.subscribe(TOPIC)
    client.loop_forever()
