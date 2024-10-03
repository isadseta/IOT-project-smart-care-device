# python 3.11

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "iotproject/mqttproject"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'





def on_connect(client, userdata, flags, rc):
    print("Connecting operation started.........")

    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
def connect_mqtt():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,client_id)
    #client.username_pw_set("sa", "1")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

def subscribe(client: mqtt_client):

    client.subscribe(topic)
    client.on_message = on_message
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
        if msg_count > 50:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client)
    client.loop_stop()

def run_sender_in_threading():
    while True:
        try:
            run()
        except Exception as ex:
            print("sender thread has error contact administrator")
            print(ex)

if __name__ == '__main__':
    run()
# import paho.mqtt.client as mqtt
# from paho.mqtt import client as mqtt_client
#
# # MQTT broker configuration
# broker_address = "your_broker_address"  # Replace with your broker's IP or hostname
# broker_port = 1883  # Default MQTT port
# client_id = "your_client_id"  # Unique identifier for your client
#
# # Callback functions
# def on_connect(client, userdata, flags, rc):
#     """Callback function for when the client connects to the broker."""
#     if rc == 0:
#         print("Connected to MQTT broker")
#         # Subscribe to topics
#         client.subscribe("your_topic")  # Replace with desired topic
#     else:
#         print("Connection failed with result code {}".format(str(rc)))
#
# def on_message(client, userdata, msg):
#     """Callback function for when a message is received."""
#     print("Received message on topic {}: {}".format(msg.topic, msg.payload.decode()))
#
# # Create MQTT client (Specify callback_api_version for compatibility)
# client = mqtt.Client(client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION1)  # Default to v1 for compatibility
#
# # Set callbacks (Not strictly necessary if using v1 API version)
# client.on_connect = on_connect
# client.on_message = on_message
#
# # Connect to the broker
# client.connect(broker_address, broker_port)
#
# # Start the network loop
# client.loop_forever()
# import sys
# #from paho.mqtt import client as mqtt_client
# import paho.mqtt.client as paho
#
# client = paho.Client(paho.CallbackAPIVersion.VERSION2,"Sender_Client")
# client.username_pw_set("sa", "1")
# if client.connect("127.0.0.1", 1883, 60) != 0:
#     print("Couldn't connect to the mqtt broker")
#     sys.exit(1)
#
# print("Successfully connection...")
# send_message_result=client.publish("test_topic", "Hi, paho mqtt client works fine!", 0)
# status = send_message_result[0]
# if status == 0:
#     print(f"Send `test_topic` to topic `Hi, paho mqtt client works fine!`")
# else:
#     print(f"Failed to send message to topic test_topic")
# print(send_message_result)
# client.disconnect()