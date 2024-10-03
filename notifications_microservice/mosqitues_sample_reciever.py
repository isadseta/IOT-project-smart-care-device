# python 3.11

import random
import time

from paho.mqtt import client as mqtt_client


broker = '127.0.0.1'
port = 1883
topic = "iotproject/mqttproject"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def on_connect(client, userdata, flags, rc):
    print("Connecting operation started...")
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
def connect_mqtt():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,client_id)
    # client.username_pw_set("sa", "ComeToSchool1367")
    #client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
def subscribe(client: mqtt_client):

    client.subscribe(topic)
    client.on_message = on_message
    print("subscribed successfully.")
def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    print("subscribed successfully.")
    client = connect_mqtt()
    #client.loop_start()
    subscribe(client)
    #publish(client)
    client.loop_forever()

def run_reciever_in_threading():
    while True:
        try:
            run()
        except Exception as ex:
            print("reciever thread has error contact administrator")
            print(ex)

if __name__ == '__main__':
    run()
#
# import sys
#
# import paho.mqtt.client as paho
#
#
# def message_handling(client, userdata, msg):
#     print(f"{msg.topic}: {msg.payload.decode()}")
#
#
# client = paho.Client(paho.CallbackAPIVersion.VERSION1,"Reciever_client")
# client.on_message = message_handling
#
# if client.connect("127.0.0.1", 1883, 60) != 0:
#     print("Couldn't connect to the mqtt broker")
#     sys.exit(1)
#
# client.subscribe("test_topic")
#
# try:
#     print("Press CTRL+C to exit...")
#     client.loop_forever()
# except Exception:
#     print("Caught an Exception, something went wrong...")
# finally:
#     print("Disconnecting from the MQTT broker")
#     client.disconnect()