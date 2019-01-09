# coding: utf-8
import sys
import os
import time
import configparser
from datetime import datetime
import json
import paho.mqtt.client as mqtt
import serial
from time import sleep

TOPIC_ROOT = "iagric/controller/J2A00101/DB7qo20z"
TOPIC_ROOT_pub = "iagric/controllerack/J2A00101/DB7qo20z"
payload = {"txid":"J2A00101-1546426464", "gwid":" J2A00101", "deviceid": " DB7qo20z", "device_name": "Smart Controller", "switch_time": "2018-12-24 14:38:00", "value": "0" }
global mqtt_client
global mqtt_client_pub
global status_value

def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_connect_pub(mqtt_client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(TOPIC_ROOT_pub)


def on_publish(mqtt_client, userdata, result):
    print("message is published")


def on_message(client, userdata, message):
    global payload_rec_json
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    print("RECIVE message")
    print("message received ", str(message.payload.decode("utf-8")))
    payload_rec_json = str(message.payload.decode("utf-8"))
    with open(dir_path + '\workfile.txt', 'w', encoding='utf-8') as f:
        f.write(payload_rec_json)

    f.closed

    print(payload_rec_json)
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def init():
    global payload_rec_value

    client_id = "smartfarm_GW"
    mqtt_client = mqtt.Client(client_id=client_id)
    mqtt_client_pub = mqtt.Client(client_id=client_id)
    payload_rec_json = ""
    curr_data = 0
    old_data = 0

    ser = serial.Serial('COM28', 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

    print(ser.is_open)

    str_check_M = '$01M\r'
    str_check_F = '$01F\r'
    str_set_ON = '#010001\r'
    str_set_OFF = '#010000\r'

    # check machine type
    ser.write(str_check_M.encode())
    sleep(1)
    while True:
        read_out = ser.readline().decode('ascii')
        if not read_out:
            sleep(1)
            continue
        else:
            break

    print(read_out)

    # check machine firmware version
    ser.write(str_check_F.encode())
    sleep(1)
    while True:
        read_out = ser.readline().decode('ascii')
        if not read_out:
            sleep(1)
            continue
        else:
            break

    print(read_out)

    # set switch to off at initial
    ser.write(str_set_OFF.encode())
    sleep(1)
    while True:
        read_out = ser.readline().decode('ascii')
        if not read_out:
            sleep(1)
            continue
        else:
            break

    print(read_out)

    global payload

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client_pub = on_connect_pub

    # If broker asks user/password.
    user = "devicegw"
    password = "Vf4pjMQrTqhP"
    mqtt_client.username_pw_set(user, password)

    print("try connect mqtt")

    try:
        mqtt_client.connect("210.200.141.214", port=1883)
        print("mqtt sub connected")
        mqtt_client.loop_start()
        print("mqtt subscribe entered loop")
        print("subscribing ")
        mqtt_client.subscribe(TOPIC_ROOT)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        data_file = dir_path + '\workfile.txt'
        print(data_file)

        while True:
            # print(payload_rec_json)
            # try:
            #     payload_rec_json
            # except NameError:
            #     print("well, it WASN'T defined after all!")
            # else:
            #     print("sure, it was defined.")

            # get the current state in server send file
            with open(dir_path + '\workfile.txt', 'r', encoding='utf-8') as f:
                data = json.load(f)

            f.close()
            print(data)
            curr_data = data['value']
            print(curr_data)

            # read old state from old state file
            with open(dir_path + '\old_state.txt', 'r', encoding='utf-8') as f:
                old_data = f.read()

            f.close()
            print("old state = " + str(old_data))

            # write curr state to old state file
            with open(dir_path + '\old_state.txt', 'w', encoding='utf-8') as f:
                f.write(curr_data)

            f.close()

            if old_data == '1':
                print("old_data switch on")
                ser.write(str_set_ON.encode())
                sleep(1)
                while True:
                    read_out = ser.readline().decode('ascii')
                    if not read_out:
                        sleep(1)
                        continue
                    else:
                        break

                print(read_out)

            else :
                ser.write(str_set_OFF.encode())
                sleep(1)
                while True:
                    read_out = ser.readline().decode('ascii')
                    if not read_out:
                        sleep(1)
                        continue
                    else:
                        break

                print(read_out)

            if curr_data == old_data:
                print("not change")
            else:
                print("data changed")
                old_data = curr_data
                send_payload = {
                    'txid': data['txid'],
                    'gwid': data['gwid'],
                    'deviceid': data['deviceid'],
                    'device_name': data['device_name'],
                    'response_time': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                    'value': old_data
                }
                print("send data: ")
                print(send_payload)
                mqtt_client.publish(topic=TOPIC_ROOT_pub, payload=json.dumps(send_payload), qos=0, retain=0)

            time.sleep(1)

    except Exception as e:
        print("MQTT Broker is not online. Connect later.")
        print(str(e))
        print("RESTART the MQTT connection")
        pass


if __name__ == '__main__':
    init()

