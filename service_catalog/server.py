import cherrypy
import json
import requests
import time
import sys
import os

from utilities.service_class import BaseService


class ServiceCatalog():
    exposed = True

    def __init__(self):
        self.catalog = BaseService()

    def GET(self, *uri, **params):
        service_url = os.environ["scd_relational_database_dao"] + "/ServiceDAL"
        service_result = requests.get(service_url)
        return service_result.text

    def POST(self, *uri):
        data_to_insert = cherrypy.request.body.read()
        converted_data = json.loads(data_to_insert)
        service_url = os.environ["scd_relational_database_dao"] + "/ServiceDAL"
        service_result = requests.post(service_url, data_to_insert)
        return service_result.text

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        Id = uri[0]
        service_url = os.environ["scd_relational_database_dao"] + "/ServiceDAL"+f"/{Id}"
        service_result = requests.delete(service_url)
        return service_result.text


if __name__ == '__main__':
    try:
        if os.environ['IP_ADDRESS'] == None:
            os.environ['IP_ADDRESS'] = "0.0.0.0"
    except:
        os.environ['IP_ADDRESS'] = "0.0.0.0"
    try:
        if os.environ['IP_PORT'] == None:
            os.environ['IP_PORT'] = "50010"
    except:
        os.environ['IP_PORT'] = "50010"
    try:
        if os.environ['environment'] == None:
            os.environ['environment'] = 'debugging'
    except:
        os.environ['environment'] = 'debugging'

    try:
        if os.environ['scd_relational_database_dao'] == None:
            os.environ['scd_relational_database_dao'] = 'http://127.0.0.1:50000'
    except:
        os.environ['scd_relational_database_dao'] = 'http://127.0.0.1:50000'
    relational_database_dal_service = ServiceCatalog()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(ServiceCatalog(), '/' + type(ServiceCatalog()).__name__, conf)
    cherrypy.config.update({'server.socket_host': relational_database_dal_service.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(relational_database_dal_service.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    #while True:
    #    time.sleep(1)
    cherrypy.engine.block()
