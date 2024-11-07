import json

from paho.mqtt import client as mqtt_client
import requests, os, time
import urllib
import random


broker = ""
port = 0
measurment_topic =""
notifications_topic =""
client_id = f'publish-{random.randint(0, 1000)}'

try:
    if os.environ['service_catalog'] == None:
        os.environ['service_catalog'] = 'http://127.0.0.1:50010'
except:
    os.environ['service_catalog'] = 'http://127.0.0.1:50010'

try:
    if os.environ['DEVICE_ID'] == None:
        os.environ['DEVICE_ID'] = '123654789'
except:
    os.environ['DEVICE_ID'] = '123654789'

device_id = os.environ['DEVICE_ID']

owner_user = None
current_logined_user = None


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
            return system_config
        except Exception as ex:
            print("==================================================================================")
            print(f"Unsuccessful loading configuration because of \n {ex}.")
            time.sleep(5)


def system_config_loader():
    system_config = reload_config()
    system_config_as_cixtionary = {}
    for service_item in system_config.json():
        print(service_item)
        system_config_as_cixtionary[service_item["service_name"]] = service_item
    print(system_config_as_cixtionary)
    return system_config_as_cixtionary


def login_into_application(username, password):
    try:
        resource_catalog_address = system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog_address = change_domain_name(
            resource_catalog_address) + "/LoginService?user_email=" + username + "&user_password=" + password
        print(resource_catalog_address)
        login_result = requests.get(resource_catalog_address)
        if login_result.status_code == 200 and login_result.text == "True":
            return True
        else:
            return False
    except Exception as ex:
        print("=============================================")
        print(f"Unsucceessfull login failed because of \n {ex}.")
        return False


def get_user_data(username):
    try:
        resource_catalog_address = system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog_address = change_domain_name(
            resource_catalog_address) + "/UsersManagerService?user_email=" + username
        print(resource_catalog_address)
        current_user_data = requests.get(resource_catalog_address)
        if current_user_data.status_code == 200 and len(json.loads(current_user_data.text))>0:
            current_user_data = json.loads(current_user_data.text)
            return current_user_data[0]
        else:
            return None
    except Exception as ex:
        print("=============================================")
        print(f"Unsucceessfull login failed because of \n {ex}.")
        return None


def register_device_on_user_devices(user_id, device_name):
    try:
        my_data_for_registration = '{"device_id":"' + device_name + '","device_owner_id":"' + str(user_id) + '"}'
        resource_catalog_address = system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog_address = change_domain_name(
            resource_catalog_address) + "/DeviceManagerService"
        registration_result = requests.post(resource_catalog_address, data=my_data_for_registration)
        return True
    except Exception as ex:
        print("==============================================================")
        print(f"Unsucceessfull device registration because of \n {ex}.")
        return False


def get_my_device_config(user_id):
    try:
        resource_catalog_address = system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog_address = change_domain_name(
            resource_catalog_address) + "/DeviceManagerService?device_id=" + user_id
        print(resource_catalog_address)
        registration_result = requests.get(resource_catalog_address)
        return json.loads(registration_result.text)
    except Exception as ex:
        print("==============================================================")
        print(f"Unsucceessfull device registration because of \n {ex}.")
        return None


def get_owner_device_data(device_id):
    try:
        resource_catalog_address = system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog_address = change_domain_name(
            resource_catalog_address) + "/UsersManagerService?user_lastname=" + device_id
        registration_result = requests.get(resource_catalog_address)
        return json.loads(registration_result.text)[0]
    except Exception as ex:
        print("==============================================================")
        print(f"Unsucceessfull device registration because of \n {ex}.")
        return None
def on_connect(client, userdata, flags, rc):
    print("Connecting operation started.........")

    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    #client.username_pw_set("sa", "1")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def simulate_heart_rate():
    heart_rate = random.randint(60, 100)
    return heart_rate


def simulate_body_temperature():
    body_temp = round(random.uniform(36.5, 37.5), 1)
    return body_temp

def publish(client, topic, msg=""):
    global device_id
    user_id=str(owner_user["id"])
    current_device_id=str(device_id)
    measurment_topic ="SCD_IOT_PROJECT/measurments/"
    msg_count = 1
    while True:
        result=None
        time.sleep(1)
        simulated_heart_rate = simulate_heart_rate()
        # if msg !="":
        #     result = client.publish(measurment_topic+user_id+"/"+device_id+"/heart", str(simulated_heart_rate))
        # else:
        #     result = client.publish(topic, f'{random.uniform(1.5, 1.9)}')

        result = client.publish(measurment_topic+user_id+"/"+device_id+"/heart", str(simulated_heart_rate))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{str(simulated_heart_rate)}` to topic `{measurment_topic+user_id+"/"+device_id+"/heart"}`")
        else:
            print(f"Failed to send message to topic {measurment_topic+user_id+"/"+device_id+"/heart"}")
        time.sleep(1)
        simulated_body_temprature = simulate_body_temperature()
        # if msg != "":
        #     result = client.publish(measurment_topic+user_id+"/"+device_id+"/temprature", str(simulated_body_temprature))
        # else:
        #     result = client.publish(topic, f'{random.uniform(1.5, 1.9)}')
        result = client.publish(measurment_topic + user_id + "/" + device_id + "/temprature",
                                str(simulated_body_temprature))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{str(simulated_body_temprature)}` to topic `{measurment_topic+user_id+"/"+device_id+"/temprature"}`")
        else:
            print(f"Failed to send message to topic {measurment_topic+user_id+"/"+device_id+"/temprature"}")
        msg_count += 1
        if msg_count > 555555:
            break

def run():
    global broker
    global port
    global measurment_topic
    global notifications_topic
    broker = "10.48.83.230"
    port = 1883
    measurment_topic ="SCD_IOT_PROJECT/measurments/"
    notifications_topic ="SCD_IOT_PROJECT/notifications/"
    client = connect_mqtt()
    client.loop_start()
    publish(client,measurment_topic+"SCD_IOT_PROJECT/notifications/1/1/")
    client.loop_stop()

if __name__ == "__main__":
    device_data = get_my_device_config(device_id)
    if device_data!=None and len(device_data) > 0:
        print(" this device is registered successfully.")
        owner_user = get_owner_device_data(device_id)
    else:
        print(" this device is not registered successfully.")
        print(" you should login at first to be able to use this device completely")
        registration_result = False
        owner_user_mail = ""
        owner_user_pass = ""

        while registration_result == False:
            owner_user_mail = input("please enter user mail:")
            owner_user_pass = input("please enter user password:")
            if login_into_application(username=owner_user_mail, password=owner_user_pass):
                registration_result = True
            else:
                print("un successfully registration.\n please try again.")

        owner_user = get_user_data(username=owner_user_mail)
        register_device_on_user_devices(owner_user["id"], device_id)

    run()
