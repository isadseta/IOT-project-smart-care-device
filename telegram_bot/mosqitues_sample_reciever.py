# python 3.11
import os
import random
import time
import requests
from paho.mqtt import client as mqtt_client
import datetime
import json
from telebot import TeleBot
import urllib
broker = ""
last_config_load=None
port = 0
measurment_topic =""
notifications_topic =""
system_config=None
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
def reload_config():
    global system_config
    # getting system configs
    service_catalog_address = os.environ['service_catalog'] + "/ServiceCatalog/summary"
    while True:
        try:
            system_config = requests.get(service_catalog_address)
            print("==================================================================================")
            print("Configuration loaded successfully.")
            print(system_config)
            break
        except Exception as ex:
            print("==================================================================================")
            print(f"Unsucceessfull loading cofiguration because of \n {ex}.")
            time.sleep(5)

def system_config_loader():
    global system_config
    reload_config()
    system_config_as_cixtionary = {}
    for service_item in system_config.json():
        print(service_item)
        system_config_as_cixtionary[service_item["service_name"]] = service_item
    print(system_config_as_cixtionary)
    return system_config_as_cixtionary
def on_connect(client, userdata, flags, rc):
    print("Connecting operation started...")
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def change_domain_name(url):
    parsed_url = urllib.parse.urlparse(url)
    port = parsed_url.port

    if port is None:
        # Default port for common protocols
        if parsed_url.scheme == "http":
            port = 80
        elif parsed_url.scheme == "https":
            port = 443
        elif parsed_url.scheme == "ftp":
            port = 21
    new_url = f"http://localhost:{port}"
    return new_url
def connect_mqtt():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
    print(client_id)
    client.username_pw_set("sa", "1")
    #client.on_connect = on_connect
    print("=====================================================")
    print(broker)
    print(port)
    client.connect(broker, port)
    return client

def process_notification(topic,message):
    print("1")
    # Your bot's API token (from BotFather)
    bot = TeleBot(token='7765834121:AAGv4Rvsh-lVhsBmjnA_cH6etECDOs1JzhU')
    print("2")
    user_id=topic.split("/")[3]

    print("3")
    current_system_config=system_config_loader()
    print("4")
    resource_catalog_microsevice_address=current_system_config['resource_catalog']['service_value']
    print("5")
    resource_catalog_microsevice_address=change_domain_name(resource_catalog_microsevice_address)+"/UsersManagerService?id="+user_id
    print("6")
    user_data=requests.get(resource_catalog_microsevice_address)
    print("7")
    user_data=json.loads(user_data.text)
    print("8")
    if len(user_data) <1:
        return
    print("10")
    if user_data[0]["user_telegram_bot_id"] == "" or user_data[0]["user_telegram_bot_id"]=="-------------":
        return
    print("11")
    user_Data_chat_id=user_data[0]["user_telegram_bot_id"]
    print("12")
    # Sending the message
    bot.send_message(user_Data_chat_id, message)
    print("13")
    print ("=======================================")
    print ("message sent to user.")

def on_message(client, userdata, msg):
    topic_parts=msg.topic.split("/")
    if topic_parts[1]=="notifications":
        process_notification(msg.topic,msg.payload.decode())
def subscribe(client: mqtt_client):
    client.subscribe(notifications_topic+"#")
    client.on_message = on_message
    time.sleep(3)

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
    print("subscribing started successfully.")
    client = connect_mqtt()
    #client.loop_start()
    subscribe(client)
    #publish(client)
    client.loop_forever()

def run_reciever_in_threading():
    global broker
    global port
    global measurment_topic
    global notifications_topic
    broker ="10.48.83.230"
    port = 1883
    notifications_topic ="SCD_IOT_PROJECT/notifications/"
    while True:
        try:
            run()
        except Exception as ex:
            print("reciever thread has error contact administrator")
            print(ex)

if __name__ == '__main__':

    try:
        if os.environ['service_catalog'] == None:
            os.environ['service_catalog'] = 'http://localhost:50010'
    except:
        os.environ['service_catalog'] = 'http://localhost:50010'

    broker = "127.0.0.1"
    port = 1883
    # broker = os.environ["mosquitto_url"]
    # port = int(os.environ["mosquitto_port"])
    measurment_topic ="SCD_IOT_PROJECT/measurments/"
    notifications_topic ="SCD_IOT_PROJECT/notifications/"
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