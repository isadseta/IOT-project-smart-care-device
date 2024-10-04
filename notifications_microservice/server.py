import threading

import cherrypy
import json
import requests
import time
import sys
import os

from mosqitues_sample_reciever import run_reciever_in_threading
from mosqitues_sample_sender import run_sender_in_threading, send_notification_on_mqtt
from utilities.service_class import BaseService, system_config


class MessagingMicroservice(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()
    def get_user_all_messages(self,user_id):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"]["service_value"] + f"/MessagesDAL?reciever_id={user_id}"
        messages=requests.get(relational_database_access_url)
        return messages.text
    def get_user_not_readen_messages(self,user_id):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"]["service_value"] + f"/MessagesDAL?reciever_id={user_id}&message_state=0"
        messages=requests.get(relational_database_access_url)
        return messages.text

    def GET(self, *uri, **params):
        if uri[0]=="user":
            return self.get_user_all_messages(uri[1])
        if uri[0]=="user_not_readen":
            return self.get_user_all_messages(uri[1])
        return None

    #sample data to send message {"sende_user_id":"123456","reciever_user_id":"","message_content":"dfgss dfg sdfg sdfg sdfg sdfg sdfg sdfg sdfg dsfg"}
    def POST(self, *uri):
        try:
            data_to_insert = cherrypy.request.body.read()
            converted_data = json.loads(data_to_insert)
            sende_user_id = converted_data["sende_user_id"]
            reciever_user_id = converted_data["reciever_user_id"]
            message_content = converted_data["message_content"]
            topic_to_send = f"notifications/{sende_user_id}/{reciever_user_id}/4"
            send_notification_on_mqtt(topic_to_send, message_content)
            # =================Sending to microservice database
            system_config = self.system_config()
            relational_database_access_url = system_config["relational_database_access"]["service_value"] + "/MessagesDAL"
            new_message_content = {
                "sender_id": sende_user_id,
                "reciever_id": reciever_user_id,
                "messagge_content": message_content,
                "message_state": "0"
            }
            save_message_result=requests.post(relational_database_access_url, json.dumps(new_message_content))
            return "True"
        except Exception as ex:
            print(ex)
            return ex

    def PUT(self, *uri):
        pass


class NotificationsMicroservice(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()

    def GET(self, *uri, **params):
        try:
            data_to_insert = cherrypy.request.body.read()
            converted_data = json.loads(data_to_insert)
            sende_user_id = converted_data["sende_user_id"]
            reciever_user_id = converted_data["reciever_user_id"]
            message_content = converted_data["message_content"]
            topic_to_send = f"notifications/{sende_user_id}/{reciever_user_id}/4"
            send_notification_on_mqtt(topic_to_send, message_content)
            # =================Sending to microservice database
            system_config = self.system_config()
            relational_database_access_url = system_config["relational_database_access"]["service_value"] + "/MessagesDAL"
            new_message_content = {
                "sender_id": sende_user_id,
                "reciever_id": reciever_user_id,
                "messagge_content": message_content,
                "message_state": "6"
            }
            print(relational_database_access_url)
            print(new_message_content)
            print(json.dumps(new_message_content))
            save_message_result=requests.post(relational_database_access_url, json.dumps(new_message_content))
            return "True"
        except Exception as ex:
            print(ex)
            return ex

    def POST(self, *uri):
        pass

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        pass


def register_me():
    global system_config
    my_port = os.environ['IP_PORT']
    my_address = os.environ['IP_ADDRESS']
    service_catalog_address = os.environ['service_catalog'] + "/ServiceCatalog"
    # registering on service catalog
    current_service_information = {"service_name": "notifications",
                                   "service_value": f"http://{'127.0.0.1' if '0.0.0.0' in my_address else my_address}:{my_port}",
                                   "last_state": "1"}
    while True:
        try:
            service_result = requests.post(service_catalog_address, json.dumps(current_service_information))
            print("==================================================================================")
            print(service_result.text)
            break
        except Exception as ex:
            print("==================================================================================")
            print(f"Unsucceessfull registration on the server because of \n {ex}.")
            time.sleep(5)


if __name__ == '__main__':

    try:
        if os.environ['mosquitto_url'] == None:
            os.environ['mosquitto_url'] = "127.0.0.1"
    except:
        os.environ['mosquitto_url'] = "127.0.0.1"


    try:
        if os.environ['mosquitto_port'] == None:
            os.environ['mosquitto_port'] = "1883"
    except:
        os.environ['mosquitto_port'] = "1883"

    try:
        if os.environ['IP_ADDRESS'] == None:
            os.environ['IP_ADDRESS'] = "0.0.0.0"
    except:
        os.environ['IP_ADDRESS'] = "0.0.0.0"
    try:
        if os.environ['IP_PORT'] == None:
            os.environ['IP_PORT'] = "50050"
    except:
        os.environ['IP_PORT'] = "50050"
    try:
        if os.environ['environment'] == None:
            os.environ['environment'] = 'debugging'
    except:
        os.environ['environment'] = 'debugging'

    try:
        if os.environ['service_catalog'] == None:
            os.environ['service_catalog'] = 'http://localhost:50010'
    except:
        os.environ['service_catalog'] = 'http://localhost:50010'

    register_me()

    x = threading.Thread(target=run_reciever_in_threading)
    x.start()

    relational_database_dal_service = NotificationsMicroservice()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }

    cherrypy.tree.mount(MessagingMicroservice(), '/' + type(MessagingMicroservice()).__name__, conf)
    cherrypy.tree.mount(NotificationsMicroservice(), '/' + type(NotificationsMicroservice()).__name__, conf)
    cherrypy.config.update({'server.socket_host': relational_database_dal_service.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(relational_database_dal_service.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    while True:
        time.sleep(1)
    cherrypy.engine.block()
