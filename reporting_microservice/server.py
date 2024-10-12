import threading

import cherrypy
import json
import requests
import time
import sys
import os
import cherrypy_cors
from utilities.service_class import BaseService, system_config

class MeaturmentsMicroservice(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()

    def GET(self, *uri, **params):
        try:
            app_config=self.system_config()
            if not "influx_db_access" in app_config.keys():
                raise Exception("the influx_db_access micro service is not registered.")
            user_id=params["user_id"]
            senser_id_prefix=params["senser_id_prefix"]
            date_days_length=params["date_days_length"]
            influx_db_access_url=app_config["influx_db_access"]["service_value"]
            reporting_parameter=uri[0]
            if reporting_parameter=='heart':
                reporting_url=influx_db_access_url+f'/HeartInfluxDbDal?user_id={user_id}&senser_id_prefix={senser_id_prefix}&date_days_length={date_days_length}'
                report_result=requests.get(reporting_url)
                return report_result.text

            if reporting_parameter=='temprature':
                reporting_url=influx_db_access_url+f'/TempratureInfluxDbDal?user_id={user_id}&senser_id_prefix={senser_id_prefix}&date_days_length={date_days_length}'
                report_result=requests.get(reporting_url)
                return report_result.text
        except Exception as ex:
            raise Exception(ex)
        return 'not found report with these parametere'



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
    current_service_information = {"service_name": "reporting",
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
        if os.environ['IP_ADDRESS'] == None:
            os.environ['IP_ADDRESS'] = "0.0.0.0"
    except:
        os.environ['IP_ADDRESS'] = "0.0.0.0"
    try:
        if os.environ['IP_PORT'] == None:
            os.environ['IP_PORT'] = "50070"
    except:
        os.environ['IP_PORT'] = "50070"
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

    cherrypy_cors.install()
    register_me()

    relational_database_dal_service = MeaturmentsMicroservice()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'cors.expose.on': True,
        }
    }

    cherrypy.tree.mount(MeaturmentsMicroservice(), '/' + type(MeaturmentsMicroservice()).__name__, conf)
    cherrypy.config.update({'server.socket_host': relational_database_dal_service.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(relational_database_dal_service.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    while True:
        time.sleep(1)
    cherrypy.engine.block()
