# coding: utf-8
import sys
import os
import time
import configparser
import paho.mqtt.client as mqtt

TOPIC_ROOT = "iagric/controller/J2A00101/DB7qo20z"
global mqtt_client


def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt_client.subscribe(TOPIC_ROOT)


def on_message(mqtt_client, userdata, message):
    print("RECIVE message")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def init():
    # define global parameters
    # global dir_path
    # global config
    #
    # # Read the config files
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)
    # config = configparser.ConfigParser()
    # print(dir_path + '\config.ini')
    # config.read(dir_path + '\config.ini')

    # # Print config information for confirm
    # print(config['MQTT-Subscriber']['HOST'])

    client_id = "smartfarm_GW"
    mqtt_client = mqtt.Client(client_id=client_id)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # If broker asks user/password.
    user = "devicegw"
    password = "Vf4pjMQrTqhP"
    mqtt_client.username_pw_set(user, password)

    print("try connect mqtt")

    try:
        mqtt_client.connect("210.200.141.214", port=1883)
        print("connected")
        print("mqtt subscribe entered loop")
        mqtt_client.loop_forever()

    except Exception as e:
        print("MQTT Broker is not online. Connect later.")
        print(str(e))


if __name__ == '__main__':
    init()

