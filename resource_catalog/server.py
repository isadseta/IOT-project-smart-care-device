import cherrypy
import json
import requests
import time
import sys
import os, random
import cherrypy_cors
from utilities.service_class import BaseService


def cors_tool():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"


cherrypy.tools.cors = cherrypy.Tool('before_handler', cors_tool)


@cherrypy.tools.cors()
class UsersManagerService(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()

    @cherrypy.tools.cors()
    def GET(self, *uri, **params):
        system_config = self.system_config()
        ralational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDAL?def_param=1"
        if 'id' in params.keys():
            ralational_database_access_url += f"&id={params['id']}"
        if 'user_name' in params.keys():
            ralational_database_access_url += f"&user_name={params['user_name']}"
        if 'user_lastname' in params.keys():
            ralational_database_access_url += f"&user_lastname={params['user_lastname']}"
        if 'user_email' in params.keys():
            ralational_database_access_url += f"&user_email={params['user_email']}"
        if 'user_type' in params.keys():
            ralational_database_access_url += f"&user_type={params['user_type']}"
        selected_users = requests.get(ralational_database_access_url).text
        return selected_users

    @cherrypy.tools.cors()
    def POST(self, *uri):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"]["service_value"] + f"/UsersDAL"
        data_to_insert = cherrypy.request.body.read()
        sending_data_result = requests.post(relational_database_access_url, data_to_insert)
        return sending_data_result.text

    @cherrypy.tools.cors()
    def PUT(self, *uri):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDAL/{uri[0]}"
        data_to_insert = cherrypy.request.body.read()
        sending_data_result = requests.put(relational_database_access_url, data_to_insert)
        return sending_data_result.text

    @cherrypy.tools.cors()
    def DELETE(self, *uri):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDAL/{uri[0]}"
        sending_data_result = requests.delete(relational_database_access_url)
        return sending_data_result.text
    @cherrypy.tools.cors()
    def OPTIONS(self, *args, **kwargs):
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return ''


class DeviceManagerService(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()
    @cherrypy.tools.cors()
    def GET(self, *uri, **params):
        system_config = self.system_config()
        ralational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDAL?def_param=1"
        ralational_database_access_url += f"&user_name=scd_device"
        if 'device_id' in params.keys():
            ralational_database_access_url += f"&user_lastname={params['device_id']}"
        if 'device_owner_id' in params.keys():
            ralational_database_access_url += f"&user_email={params['device_owner_id']}"
        ralational_database_access_url += f"&user_type=4"
        selected_users = requests.get(ralational_database_access_url).text
        return selected_users
    @cherrypy.tools.cors()
    def POST(self, *uri):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"]["service_value"] + f"/UsersDAL"
        data_to_insert = cherrypy.request.body.read()
        converted_posted_data = json.loads(data_to_insert)
        converted_posted_data["user_name"] = "scd_device"
        converted_posted_data["user_lastname"] = converted_posted_data["device_id"]
        converted_posted_data["user_email"] = converted_posted_data["device_owner_id"]
        converted_posted_data["user_password"] = "------------"
        converted_posted_data["user_hashed_password"] = "------------"
        converted_posted_data["user_type"] = "4"
        converted_posted_data["user_telegram_bot_id"] = "-------------"
        sending_data_result = requests.post(relational_database_access_url, json.dumps(converted_posted_data))
        return sending_data_result.text

    @cherrypy.tools.cors()
    def PUT(self, *uri):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDAL/{uri[0]}"
        data_to_insert = cherrypy.request.body.read()
        converted_posted_data = json.loads(data_to_insert)
        converted_posted_data["user_name"] = "scd_device"
        converted_posted_data["user_lastname"] = converted_posted_data["device_id"]
        converted_posted_data["user_email"] = converted_posted_data["device_owner_id"]
        converted_posted_data["user_password"] = "------------"
        converted_posted_data["user_hashed_password"] = "------------"
        converted_posted_data["user_type"] = "4"
        sending_data_result = requests.put(relational_database_access_url, json.dumps(converted_posted_data))
        return sending_data_result.text

    def DELETE(self, *uri):
        system_config = self.system_config()
        relational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDAL/{uri[0]}"
        sending_data_result = requests.delete(relational_database_access_url)
        return sending_data_result.text
    @cherrypy.tools.cors()
    def OPTIONS(self, *args, **kwargs):
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return ''


class LoginService(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()
    @cherrypy.tools.cors()
    def GET(self, *uri, **params):
        system_config = self.system_config()
        ralational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDAL?def_param=1"
        ralational_database_access_url += f"&user_email={params['user_email']}"
        selected_users = requests.get(ralational_database_access_url).text
        print(selected_users)
        if len(json.loads(selected_users)) > 0 and json.loads(selected_users)[0]["user_password"] == params[
            'user_password']:
            return "True"
        return "False"
    @cherrypy.tools.cors()
    def OPTIONS(self, *args, **kwargs):
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return ''




@cherrypy.tools.cors()
class UsersDoctorsRelationService(BaseService):
    exposed = True

    def __init__(self):
        self.catalog = BaseService()
    @cherrypy.tools.cors()
    def GET(self, *uri, **params):
        system_config = self.system_config()
        ralational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDoctorsDAL?def_param=1"
        if 'docter_user_id' in params.keys():
            ralational_database_access_url += f"&docter_user_id={params['docter_user_id']}"
        if 'sick_user_id' in params.keys():
            ralational_database_access_url += f"&sick_user_id={params['sick_user_id']}"
        selected_relations = requests.get(ralational_database_access_url).text
        return selected_relations
    @cherrypy.tools.cors()
    def POST(self, *uri, **params):
        print("===========================================")
        print("OPeration started")
        system_config = self.system_config()
        print("===========================================")
        print("Config loaded")
        ralational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDoctorsDAL"
        print("===========================================")
        print("Url of posting data:"+ralational_database_access_url)
        data_to_insert = cherrypy.request.body.read()
        print("===========================================")
        print(data_to_insert)
        converted_data = json.loads(data_to_insert)
        print("===========================================")
        print(converted_data)
        sending_data_result = requests.post(ralational_database_access_url, data_to_insert)
        return sending_data_result.text
    @cherrypy.tools.cors()
    def OPTIONS(self, *args, **kwargs):
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return ''

    '''
    1(relation):delete only one user doctor relation
    2(docktor_sick_people):delete all of users doctor relations of doctor
    3(sick_people_doctor):delete all users doctor relations of users
    '''

    def DELETE(self, *uri):
        system_config = self.system_config()
        ralational_database_access_url = system_config["relational_database_access"][
                                             "service_value"] + f"/UsersDoctorsDAL"
        if uri[0] == "relation":
            ralational_database_access_url += f"/1/{uri[1]}"
            request_result = requests.delete(ralational_database_access_url)
            return request_result
        if uri[0] == "docktor_sick_people":
            ralational_database_access_url += f"/2/{uri[1]}"
            request_result = requests.delete(ralational_database_access_url)
            return request_result
        if uri[0] == "sick_people_doctors":
            ralational_database_access_url += f"/3/{uri[1]}"
            request_result = requests.delete(ralational_database_access_url)
            return request_result


def register_me():
    global system_config
    my_port = os.environ['IP_PORT']
    my_address = os.environ['IP_ADDRESS']
    service_catalog_address = os.environ['service_catalog'] + "/ServiceCatalog"
    # registering on service catalog
    current_service_information = {"service_name": "resource_catalog",
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
            print(f"Unsuccessfully registration on the server because of \n {ex}.")
            time.sleep(5)


if __name__ == '__main__':
    try:
        if os.environ['IP_ADDRESS'] == None:
            os.environ['IP_ADDRESS'] = "0.0.0.0"
    except:
        os.environ['IP_ADDRESS'] = "0.0.0.0"
    try:
        if os.environ['IP_PORT'] == None:
            os.environ['IP_PORT'] = "60090"
    except:
        os.environ['IP_PORT'] = "60090"
    try:
        if os.environ['environment'] == None:
            os.environ['environment'] = 'debugging'
    except:
        os.environ['environment'] = 'debugging'
    try:
        if os.environ['service_catalog'] == None:
            os.environ['service_catalog'] = 'http://127.0.0.1:50010'
    except:
        os.environ['service_catalog'] = 'http://127.0.0.1:50010'
    base_class_to_retrive_microservice_information = UsersManagerService() 
    
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.cors.on': True
        }
    }

    register_me()

    cherrypy.tools.cors = cherrypy.Tool('before_handler', cors_tool)
    print("=======================================================================")
    print("starting  the server.")
    cherrypy.tree.mount(LoginService(), '/' + type(LoginService()).__name__, conf)
    cherrypy.tree.mount(UsersManagerService(), '/' + type(UsersManagerService()).__name__, conf)
    cherrypy.tree.mount(DeviceManagerService(), '/' + type(DeviceManagerService()).__name__, conf)
    cherrypy.tree.mount(UsersDoctorsRelationService(), '/' + type(UsersDoctorsRelationService()).__name__, conf)
    cherrypy.config.update(
        {'server.socket_host': base_class_to_retrive_microservice_information.catalog.serviceCatalogIP})
    cherrypy.config.update(
        {'server.socket_port': int(base_class_to_retrive_microservice_information.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    #while True:
    #    time.sleep(1)
    cherrypy.engine.block()
