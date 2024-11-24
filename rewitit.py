import os
import random
import time
import requests
import json
from paho.mqtt import client as mqtt_client

# Configuration variables
BROKER = os.getenv("mosquitto_url", "127.0.0.1")
PORT = int(os.getenv("mosquitto_port", 1883))
MEASUREMENT_TOPIC = "SCD_IOT_PROJECT/measurments/"
NOTIFICATIONS_TOPIC = "SCD_IOT_PROJECT/notifications/"
SERVICE_CATALOG = os.getenv("service_catalog", "http://localhost:50010/ServiceCatalog/summary")
CLIENT_ID = f'client-{random.randint(0, 1000)}'

system_config = None

def load_config():
    """Load system configuration from the service catalog."""
    global system_config
    while True:
        try:
            response = requests.get(SERVICE_CATALOG)
            response.raise_for_status()
            system_config = {item["service_name"]: item for item in response.json()}
            print("System configuration loaded successfully.")
            return
        except Exception as ex:
            print(f"Error loading system configuration: {ex}")
            time.sleep(5)

def connect_mqtt():
    """Connect to the MQTT broker."""
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = lambda client, userdata, flags, rc: print(
        "Connected to MQTT Broker!" if rc == 0 else f"Failed to connect, return code {rc}"
    )
    client.connect(BROKER, PORT)
    return client

def process_measurement(topic, message):
    """Process measurement messages and handle alerts."""
    try:
        global system_config
        if not system_config:
            load_config()

        topic_parts = topic.split("/")
        measurement_type = topic_parts[4]
        user_id = topic_parts[2]

        user_service_url = f"{system_config['resource_catalog']['service_value']}/UsersManagerService?id={user_id}"
        user_info = requests.get(user_service_url).json()

        measurement_value = float(message)
        alert_needed = False

        if measurement_type == "temprature":
            if not (user_info["min_body_temprature"] <= measurement_value <= user_info["max_body_temprature"]):
                alert_needed = True
        elif measurement_type == "heart_rate":
            if not (user_info["min_heart_rate"] <= measurement_value <= user_info["max_heart_rate"]):
                alert_needed = True

        if alert_needed:
            alert_doctor(user_id, user_info, measurement_type, measurement_value)

    except Exception as ex:
        print(f"Error processing measurement: {ex}")

def alert_doctor(user_id, user_info, measurement_type, measurement_value):
    """Send an alert to the doctor."""
    try:
        global system_config
        doctor_service_url = f"{system_config['resource_catalog']['service_value']}/UsersDoctorsRelationService?sick_user_id={user_id}"
        doctor_info = requests.get(doctor_service_url).json()

        notification_service_url = f"{system_config['notifications']['service_value']}/MessagingMicroservice"
        notification_message = {
            "sende_user_id": user_id,
            "reciever_user_id": doctor_info["docter_user_id"],
            "message_content": f"Alert for {user_info['user_lastname']} {user_info['user_name']}: {measurement_type} value {measurement_value} out of range."
        }
        requests.post(notification_service_url, json=notification_message)
        print("Alert sent to doctor.")
    except Exception as ex:
        print(f"Error sending alert: {ex}")

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages."""
    topic = msg.topic
    message = msg.payload.decode()
    print(f"Received `{message}` from `{topic}` topic")
    
    if topic.startswith(MEASUREMENT_TOPIC):
        process_measurement(topic, message)
    elif topic.startswith(NOTIFICATIONS_TOPIC):
        print("Processing notification (not implemented)")

def subscribe(client):
    """Subscribe to MQTT topics."""
    client.subscribe(f"{MEASUREMENT_TOPIC}#")
    client.subscribe(f"{NOTIFICATIONS_TOPIC}#")
    client.on_message = on_message
    print("Subscribed to topics.")

def run():
    """Run the MQTT client."""
    load_config()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
