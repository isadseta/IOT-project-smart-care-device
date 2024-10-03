import threading

import cherrypy
import json
import requests
import time
import sys
import os

from mosqitues_sample_reciever import run_reciever_in_threading
from mosqitues_sample_sender import run_sender_in_threading
from utilities.service_class import BaseService


class NotificationsMicroservice(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()

    def GET(self, *uri, **params):
        return json.dumps({"message":"system is working"})

    def POST(self, *uri):
        pass

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        pass


if __name__ == '__main__':

    x = threading.Thread(target=run_sender_in_threading)
    x.start()

    x = threading.Thread(target=run_reciever_in_threading)
    x.start()

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
        if os.environ['scd_relational_database_dao'] == None:
            os.environ['scd_relational_database_dao'] = 'http://127.0.0.1:50050'
    except:
        os.environ['scd_relational_database_dao'] = 'http://127.0.0.1:50050'
    relational_database_dal_service = NotificationsMicroservice()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(NotificationsMicroservice(), '/' + type(NotificationsMicroservice()).__name__, conf)
    cherrypy.config.update({'server.socket_host': relational_database_dal_service.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(relational_database_dal_service.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    while True:
        time.sleep(1)
    cherrypy.engine.block()
