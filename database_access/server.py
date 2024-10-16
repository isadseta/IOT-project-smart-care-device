import cherrypy
import json
import requests
import time
import sys
import os
import psycopg2
import cherrypy_cors

from utilities.database_schema import tables_creation
from utilities.db_tools import fetch_list, execute_query, create_database_query
from utilities.service_class import RelationalDatabaseDAL


class ServiceDAL():
    exposed = True

    def __init__(self):
        self.catalog = RelationalDatabaseDAL()

    def GET(self, *uri, **params):
        for item in params:
            print(item)
        query = 'SELECT id,service_name,service_value,last_usage,last_state FROM service_catalog '
        where_claus = ""
        if 'name' in params.keys():
            where_claus += f" and service_name like '%{params['name']}%' "
        if 'last_state' in params.keys():
            where_claus += f" and last_state = {params['name']} "
        if len(where_claus) > 0:
            query += ' where 1=1 ' + where_claus
        fetched_rows = fetch_list(query)
        result = []
        for item in fetched_rows:
            result.append({"id": item[0], "service_name": item[1], "service_value": item[2], "last_usage": item[3],
                           "last_state": item[4]})
        return json.dumps(result, indent=4, sort_keys=True, default=str)

    def POST(self, *uri):
        data_to_insert = cherrypy.request.body.read()
        converted_data = json.loads(data_to_insert)
        query = " insert into service_catalog (service_name,service_value,last_state) values ('" + converted_data[
            "service_name"] + "','" + converted_data["service_value"] + "'," + converted_data["last_state"] + ")"
        print(query)
        result = execute_query(query)
        print(result)
        return json.dumps(result)

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        query = ""
        try:

            query = f"""
                Delete from service_catalog where Id={uri[0]}
            """
            execute_query(query)
        except:
            print("==================================================")
            print("unsuccessfully query")
            print(query)
        return json.dumps(True)



class SystemConfigDal():
    exposed = True

    def __init__(self):
        self.catalog = RelationalDatabaseDAL()

    def GET(self, *uri):
        query = f"""
            select id,service_name,service_value,last_usage,last_state from service_catalog where last_usage in
                (select max(last_usage) from service_catalog
                GROUP BY service_name)
        """
        query_rersult = fetch_list(query)
        result = []
        for item in query_rersult:
            result.append({"id": item[0], "service_name": item[1], "service_value": item[2], "last_usage": item[3],
                           "last_state": item[4]})
        return json.dumps(result, indent=4, sort_keys=True, default=str)


class UsersDAL():
    exposed = True

    def __init__(self):
        self.catalog = RelationalDatabaseDAL()

    def GET(self, *uri, **params):
        for item in params:
            print(item)
        query = 'SELECT id,user_name,user_lastname,user_email,user_password,user_hashed_password,user_type,user_telegram_bot_id FROM users_table '
        where_claus = ""
        if 'id' in params.keys():
            where_claus += f" and id = {params['id']} "
        if 'user_name' in params.keys():
            where_claus += f" and user_name like '%{params['user_name']}%' "
        if 'user_lastname' in params.keys():
            where_claus += f" and user_lastname like '%{params['user_lastname']}%' "
        if 'user_telegram_bot_id' in params.keys():
            where_claus += f" and user_telegram_bot_id like '%{params['user_telegram_bot_id']}%' "
        if 'user_email' in params.keys():
            where_claus += f" and user_email like '%{params['user_email']}%' "
        if 'user_type' in params.keys():
            where_claus += f" and user_type = {params['user_type']} "
        if len(where_claus) > 0:
            query += ' where 1=1 ' + where_claus
        fetched_rows = fetch_list(query)
        result = []
        for item in fetched_rows:
            result.append({"id": item[0], "user_name": item[1], "user_lastname": item[2], "user_email": item[3],
                           "user_password": item[4], "user_hashed_password": item[5], "user_type": item[6],"user_telegram_bot_id":item[7]})
        return json.dumps(result, indent=4, sort_keys=True, default=str)

    def POST(self, *uri):
        data_to_insert = cherrypy.request.body.read()
        converted_data = json.loads(data_to_insert)
        query = (
                    " insert into users_table (user_name,user_lastname,user_email,user_password,user_hashed_password,user_type,user_telegram_bot_id) values ('"
                    + converted_data["user_name"] +
                    "','" + converted_data["user_lastname"] +
                    "','" + converted_data["user_email"] +
                    "','" + converted_data["user_password"] +
                    "','" + converted_data["user_hashed_password"] +
                    "'," + converted_data["user_type"] +
                    ",'" + converted_data["user_telegram_bot_id"] + "' )")
        print(query)
        result = execute_query(query)
        print(result)
        return json.dumps(result)

    def PUT(self, *uri):
        select_id=uri[0]
        data_to_insert = cherrypy.request.body.read()
        converted_data = json.loads(data_to_insert)
        if select_id.isnumeric()==False :
            raise Exception("url params does not contains valid id to be updated.")
        query=f'''
        update users_table
        SET  
            user_name= '{converted_data["user_name"]}'
            ,user_lastname = '{converted_data["user_lastname"]}'
            ,user_email= N'{converted_data["user_email"]}'    
            ,user_password='{converted_data["user_password"]}'
            ,user_hashed_password='{converted_data["user_hashed_password"]}'
            ,user_type='{converted_data["user_type"]}'
            ,user_telegram_bot_id='{converted_data["user_telegram_bot_id"]}'
        WHERE ID={select_id}'''
        try:
            execute_query(query)
        except:
            print("==================================================")
            print("unsuccessfully query")
            print(query)

            return json.dumps(False)
        return json.dumps(True)

    def DELETE(self, *uri):
        query = ""
        try:

            query = f"""
                Delete from users_table where Id={uri[0]}
            """
            execute_query(query)
        except:
            print("==================================================")
            print("unsuccessfully query")
            print(query)
        return json.dumps(True)

class MessagesDAL():
    exposed = True

    def __init__(self):
        self.catalog = RelationalDatabaseDAL()

    def GET(self, *uri, **params):
        for item in params:
            print(item)
        query = 'SELECT id,sender_id,reciever_id,messagge_content,message_state,creation_date FROM messages_table '
        where_claus = ""
        if 'messagge_content' in params.keys():
            where_claus += f" and messagge_content like '%{params['messagge_content']}%' "
        if 'sender_id' in params.keys():
            where_claus += f" and sender_id = {params['sender_id']} "
        if 'reciever_id' in params.keys():
            where_claus += f" and reciever_id = {params['reciever_id']} "
        if 'message_state' in params.keys():
            where_claus += f" and message_state = {params['message_state']} "
        if len(where_claus) > 0:
            query += ' where 1=1 ' + where_claus
        fetched_rows = fetch_list(query)
        result = []
        for item in fetched_rows:
            result.append({"id": item[0], "sender_id": item[1], "reciever_id": item[2], "messagge_content": item[3],
                           "message_state": item[4],"creation_date": item[5]})
        return json.dumps(result, indent=4, sort_keys=True, default=str)

    def POST(self, *uri):
        data_to_insert = cherrypy.request.body.read()
        converted_data = json.loads(data_to_insert)
        query = (
                    " insert into messages_table (sender_id,reciever_id,messagge_content,message_state) values ("
                    + str(converted_data["sender_id"]) +
                    "," + str(converted_data["reciever_id"]) +
                    ",N'" + converted_data["messagge_content"] +
                    "'," + str(converted_data["message_state"]) +")")
        print(query)
        result = execute_query(query)
        print(result)
        return json.dumps(result)

    def PUT(self, *uri):
        select_id=uri[0]
        data_to_insert = cherrypy.request.body.read()
        converted_data = json.loads(data_to_insert)
        if select_id.isnumeric()==False :
            raise Exception("url params does not contains valid id to be updated.")
        query=f'''
        update messages_table
        SET  
            sender_id= {converted_data["sender_id"]}
            ,reciever_id = {converted_data["reciever_id"]}
            ,messagge_content= N'{converted_data["messagge_content"]}'    
            ,message_state={converted_data["message_state"]}
        WHERE ID={select_id}'''
        try:
            execute_query(query)
        except:
            print("==================================================")
            print("unsuccessfully query")
            print(query)

            return json.dumps(False)
        return json.dumps(True)
    def DELETE(self, *uri):
        query = ""
        try:

            query = f"""
                Delete from messages_table where Id={uri[0]}
            """
            execute_query(query)
        except:
            print("==================================================")
            print("unsuccessfully query")
            print(query)
        return json.dumps(True)

class UsersDoctorsDAL():
    exposed = True

    def __init__(self):
        self.catalog = RelationalDatabaseDAL()

    def GET(self, *uri, **params):
        for item in params:
            print(item)
        query = '''SELECT udr.id,docter_user_id,doctors.user_lastname||' '||doctors.user_name doctor_name,
                   sick_user_id,sicks.user_lastname||' '||sicks.user_name sick_name FROM users_doctors_table udr
                    inner join users_table doctors on doctors.id=udr.docter_user_id
                    inner join users_table sicks on sicks.id = udr.sick_user_id'''
        where_claus = ""
        if 'docter_user_id' in params.keys():
            where_claus += f" and docter_user_id = '{params['docter_user_id']}' "
        if 'sick_user_id' in params.keys():
            where_claus += f" and sick_user_id = '{params['sick_user_id']}' "
        if len(where_claus) > 0:
            query += ' where 1=1 ' + where_claus
        fetched_rows = fetch_list(query)
        result = []
        for item in fetched_rows:
            result.append({"id": item[0], "docter_user_id": item[1],"doctor_name":item[2], "sick_user_id": item[3],"sick_user_name":item[4]})
        return json.dumps(result, indent=4, sort_keys=True, default=str)

    def POST(self, *uri):
        print("===================================")
        print("Updating users started")
        data_to_insert = cherrypy.request.body.read()
        print(data_to_insert)
        converted_data = json.loads(data_to_insert)
        print(converted_data)
        query = (
                    " insert into users_doctors_table (docter_user_id,sick_user_id) values ("
                    + str(converted_data["docter_user_id"]) +
                    "," + str(converted_data["sick_user_id"]) + ")")
        print(query)
        result = execute_query(query)
        print(result)
        return json.dumps(result)

    def PUT(self, *uri):
        pass
    '''
    1:delete only one user doctor relation
    2:delete all of users doctor relations of doctor
    3:delete all users doctor relations of users
    '''
    def DELETE(self, *uri):
        operation_code=uri[0]
        selected_id = uri[1]
        query = ""
        if operation_code=='1':
            query = f"""
                Delete from users_doctors_table where Id={selected_id}
            """
        if operation_code=='2':
            query = f"""
                Delete from users_doctors_table where docter_user_id={selected_id}
            """
        if operation_code=='3':
            query = f"""
                Delete from users_doctors_table where sick_user_id={selected_id}
            """
        try:

            execute_query(query)
        except:
            print("==================================================")
            print("unsuccessfully query")
            print(query)
        return json.dumps(True)

class OtherClassDall():
    exposed = True

    def __init__(self):
        self.catalog = RelationalDatabaseDAL()

    def GET(self, *uri):
        return {'status OtherClassDall': 'OK'}

    def POST(self, *uri):
        return {'status 2 OtherClassDall': 'OK'}

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        pass

def register_me():
    global system_config
    my_port = os.environ['IP_PORT']
    my_address = os.environ['IP_ADDRESS']
    while True:
        try:
            query = (" insert into service_catalog (service_name,service_value,last_state) values ('relational_database_access'"
                     ",'") + f"http://{'127.0.0.1' if '0.0.0.0'in my_address else my_address }:{my_port}" + "',1)"
            print(query)
            result = execute_query(query)

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
            os.environ['IP_PORT'] = "50000"
    except:
        os.environ['IP_PORT'] = "50000"
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
    relational_database_dal_service = OtherClassDall()
    cherrypy_cors.install()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'cors.expose.on': True,
        }
    }
    #try:
    #    create_database_query("CREATE DATABASE test_schema")
    #except :
    #    raise
    tables_creation()
    register_me()
    cherrypy.tree.mount(MessagesDAL(), '/' + type(MessagesDAL()).__name__, conf)
    cherrypy.tree.mount(UsersDAL(), '/' + type(UsersDAL()).__name__, conf)
    cherrypy.tree.mount(UsersDoctorsDAL(), '/' + type(UsersDoctorsDAL()).__name__, conf)
    cherrypy.tree.mount(SystemConfigDal(), '/' + type(SystemConfigDal()).__name__, conf)
    cherrypy.tree.mount(ServiceDAL(), '/' + type(ServiceDAL()).__name__, conf)
    cherrypy.tree.mount(OtherClassDall(), '/' + type(OtherClassDall()).__name__, conf)
    cherrypy.config.update({'server.socket_host': relational_database_dal_service.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(relational_database_dal_service.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    #while True:
    #    time.sleep(1)
    cherrypy.engine.block()
