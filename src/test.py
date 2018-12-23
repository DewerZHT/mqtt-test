# coding: utf-8
import sys
import os
import time
import paho.mqtt.client as mqtt

def init():
    global mqtt_client

    client_id = "smartfarm_GW"

    mqtt_client = mqtt.Client(client_id=client_id)

    # If broker asks user/password.
    user = ""
    password = "Vf4pjMQrTqhP"
    mqtt_client.username_pw_set(user, password)

    print("try connect mqtt")

    try:
        mqtt_client.connect("210.200.141.214", 1883)
        print("connected")

    except Exception as e:
        print("MQTT Broker is not online. Connect later.")
        print(str(e))


if __name__ == '__main__':
    init()

