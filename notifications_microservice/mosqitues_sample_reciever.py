# python 3.11
import os
import random
import time
import requests
from paho.mqtt import client as mqtt_client
import datetime
import json

broker = ""
last_config_load = None
port = 0
measurment_topic = ""
notifications_topic = ""
system_config = None
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


def connect_mqtt():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
    # client.username_pw_set("sa", "ComeToSchool1367")
    # client.on_connect = on_connect
    client.connect(broker, port)
    return client


def process_measurment(topic, message):
    current_system_config = system_config_loader()
    influx_db_access_microservice_service_address = current_system_config['influx_db_access']['service_value']
    notifications_microservice_service_address = current_system_config['notifications']['service_value']
    user_information_service_url = current_system_config['resource_catalog']['service_value']
    topic_parts = topic.split('/')
    meassurment_type = topic_parts[4]
    meassurment_user_id = topic_parts[2]
    meassurment_device_id = topic_parts[3]
    user_information_service_url += "/UsersManagerService?id=" + meassurment_user_id
    user_information = requests.get(user_information_service_url).json()
    messurment_value = float(message)
    need_messaging = False
    if user_information["max_body_temprature"]== None or user_information["max_body_temperature"]== "" or user_information["min_body_temprature"]== None or user_information["min_body_temprature"]== "":
        return

    if user_information["max_heart_rate"]== None or user_information["max_heart_rate"]== "" or user_information["min_heart_rate"]== None or user_information["min_heart_rate"]== "":
        return

    if meassurment_type == "temprature":
        if user_information["max_body_temprature"] < messurment_value or user_information[
            "min_body_temprature"] > messurment_value:
            need_messaging = True
    else:
        if user_information["max_heart_rate"] < messurment_value or user_information[
            "min_heart_rate"] > messurment_value:
            need_messaging = True
    if need_messaging :
        message_content=f'urgent state for user {user_information["user_lastname"]} {user_information["user_name"]} \n this message is automatically generated and sent by system.'
        user_information_service_url=  current_system_config['resource_catalog']['service_value']
        user_information_service_url+="/UsersDoctorsRelationService?sick_user_id="+str(meassurment_user_id)
        doctor_information = requests.get(user_information_service_url).json()
        docter_user_id=doctor_information["docter_user_id"]
        notification_message_content=f'{"sende_user_id":"{meassurment_user_id}","reciever_user_id":"{docter_user_id}","message_content":"{message_content}"}'
        notifications_microservice_service_address+='/MessagingMicroservice'
        post_result=requests.post(notifications_microservice_service_address, data=notification_message_content)
    # data_to_send={"user_id":meassurment_user_id,"sensor_id":meassurment_device_id,"value":message}
    # influx_db_access_microservice_service_address=influx_db_access_microservice_service_address.replace("scd-influxdb-dal","127.0.0.1")
    # post_result=requests.post(influx_db_access_microservice_service_address,json.dumps(data_to_send))
    print("10")


def process_notification(topic, message):
    pass


def on_message(client, userdata, msg):
    # topic_parts=msg.topic.split("/")
    # if topic_parts[1]=="measurments":
    #     process_measurment(msg.topic,msg.payload.decode())
    # else:
    #     process_notification(msg.topic,msg.payload.decode())
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def subscribe(client: mqtt_client):
    client.subscribe(measurment_topic + "#")
    client.subscribe(notifications_topic + "#")
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
    print("subscribing started successfully.")
    client = connect_mqtt()
    print("subscribing started successfully 1.")
    # client.loop_start()
    subscribe(client)
    print("subscribing started successfully 2.")
    # publish(client)
    client.loop_forever()
    print("subscribing started successfully 3.")


def run_reciever_in_threading():
    global broker
    global port
    global measurment_topic
    global notifications_topic
    broker = os.environ["mosquitto_url"]
    port = int(os.environ["mosquitto_port"])
    measurment_topic ="SCD_IOT_PROJECT/measurments/"
    notifications_topic ="SCD_IOT_PROJECT/notifications/"
    while True:
        try:
            run()
        except Exception as ex:
            print("reciever thread has error contact administrator")
            print(ex)

if __name__ == '__main__':
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