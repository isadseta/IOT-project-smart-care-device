import cherrypy
import json
import requests
import time
import sys
import os
import psycopg2

from utilities.db_tools import fetch_list, execute_query, create_database_query
from utilities.service_class import RelationalDatabaseDAL


class ServiceDAL():
    exposed = True

    def __init__(self):
        self.catalog = RelationalDatabaseDAL()

    def GET(self, *uri, **params):
        for item in params:
            print(item)
        query = 'SELECT * FROM service_catalog '
        where_claus = ""
        if 'name' in params.keys():
            where_claus += f' and service_name like %{params['name']}% '
        if 'last_state' in params.keys():
            where_claus += f' and last_state = {params['name']} '
        if len(where_claus) > 0:
            query += ' where 1=1 ' + where_claus
        fetched_rows = fetch_list(query)
        result = []
        for item in fetched_rows:
            result.append({"id": item[0], "service_name": item[1], "last_usage": item[2], "last_state": item[3]})
        return json.dumps(result, indent=4, sort_keys=True, default=str)

    def POST(self, *uri):
        data_to_insert = cherrypy.request.body.read()
        converted_data = json.loads(data_to_insert)
        query = " insert into service_catalog (service_name,last_state) values ('" + converted_data[
            "service_name"] + "'," + converted_data["last_state"] + ")"
        print(query)
        result = execute_query(query)
        print(result)
        return json.dumps(result)

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        try:
            query = f"""
                Delete from service_catalog where Id={uri[0]}
            """
            execute_query(query)
        except:
            pass
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

    relational_database_dal_service = OtherClassDall()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    #try:
    #    create_database_query("CREATE DATABASE test_schema")
    #except :
    #    raise
    try:
        query = """
        CREATE TABLE IF NOT EXISTS service_catalog
            (
                id           bigint generated always as identity (minvalue 0),
                service_name varchar,
                last_usage   timestamp default now(),
                last_state   char
            );
        """
        execute_query(query)
    except:
        pass
    cherrypy.tree.mount(ServiceDAL(), '/' + type(ServiceDAL()).__name__, conf)
    cherrypy.tree.mount(OtherClassDall(), '/' + type(OtherClassDall()).__name__, conf)
    cherrypy.config.update({'server.socket_host': relational_database_dal_service.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(relational_database_dal_service.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    #while True:
    #    time.sleep(1)
    cherrypy.engine.block()
