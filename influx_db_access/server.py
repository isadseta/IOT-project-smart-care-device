import cherrypy
import json
import requests
import time
import sys
import os, random
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from utilities.service_class import BaseService
import cherrypy_cors


def initialize_influx_connection():
    result = {}
    if os.environ['environment'] == 'debugging':
        result["org"] = "IOT"
        result["url"] = "http://frosty_faraday:8086"
        result["token"] = "o-nwir-c0VQl8Q7i4w7e30xRKaVCE5ooF5w3s3e1Cpc7tkncQk7OBJpSGVMqGMB0JDq2yGM7SSZaP72XDDcdhw=="
        result["bucket"] = "IOT_SCD_PROJECT"
    else:
        result["org"] = os.environ["SCD_INFLUXDB_DAL_ORG"]
        result["url"] = os.environ["SCD_INFLUXDB_DAL_INFLUXDB_URL"]
        result["token"] = os.environ["SCD_INFLUXDB_DAL_INFLUXDB_TOCKEN"]
        result["bucket"] = os.environ["SCD_INFLUXDB_DAL_INFLUXDB_BUCKET"]
    print("------------------------------------------------------------------------------------------")
    print(result)
    return result


class HeartInfluxDbDal():
    exposed = True

    def __init__(self):
        self.catalog = BaseService()

    def GET(self, *uri, **params):
        if len(params) != 3:
            raise Exception("Bad parameter count sent.")
        user_id=params["user_id"]
        senser_id_prefix=params["senser_id_prefix"]
        date_days_length=params["date_days_length"]
        influx_db_server_config = initialize_influx_connection()

        read_client = influxdb_client.InfluxDBClient(url=influx_db_server_config["url"], token=influx_db_server_config["token"], org=influx_db_server_config["org"])

        query_api = read_client.query_api()
        query = f'''
        import "strings"
        from(bucket:"IOT_SCD_PROJECT")
                |> range(start: -{date_days_length}d, stop: now())
                |> filter(fn: (r) => r._measurement == "heart")
                |> filter(fn: (r) => r.user_id == "{user_id}")
                |> filter(fn: (r) => strings.hasPrefix(v: r.sensor_id, prefix: "{senser_id_prefix}"))
        '''
        tables = query_api.query(query, org=influx_db_server_config["org"])
        return tables.to_json()
    def POST(self, *uri):
        try:
            data_to_insert = cherrypy.request.body.read()
            converted_data = json.loads(data_to_insert)
            print(data_to_insert)
            influx_db_server_config = initialize_influx_connection()
            write_client = influxdb_client.InfluxDBClient(url=influx_db_server_config["url"],
                                                          token=influx_db_server_config["token"],
                                                          org=influx_db_server_config["org"])
            write_api = write_client.write_api(write_options=SYNCHRONOUS)
            point = (
                Point("heart")
                .tag("user_id", converted_data["user_id"])
                .tag("sensor_id", converted_data["sensor_id"])
                .field("value", converted_data["value"])
            )
            write_api.write(bucket=influx_db_server_config["bucket"], org=influx_db_server_config["org"], record=point)
            return json.dumps({"result": "successful", "operation_successfull": True})
        except Exception as e:
            print(e)
            return json.dumps({"result": "unsuccessful", "operation_successfull": False})

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        pass

class TempratureInfluxDbDal():
    exposed = True

    def __init__(self):
        self.catalog = BaseService()

    def GET(self, *uri, **params):
        if len(params) != 3:
            raise Exception("Bad parameter count sent.")
        user_id = params["user_id"]
        senser_id_prefix = params["senser_id_prefix"]
        date_days_length = params["date_days_length"]
        influx_db_server_config = initialize_influx_connection()

        read_client = influxdb_client.InfluxDBClient(url=influx_db_server_config["url"],
                                                     token=influx_db_server_config["token"],
                                                     org=influx_db_server_config["org"])

        query_api = read_client.query_api()
        query = f'''
        import "strings"
        from(bucket:"IOT_SCD_PROJECT")
                |> range(start: -{date_days_length}d, stop: now())
                |> filter(fn: (r) => r._measurement == "temprature")
                |> filter(fn: (r) => r.user_id == "{user_id}")
                |> filter(fn: (r) => strings.hasPrefix(v: r.sensor_id, prefix: "{senser_id_prefix}"))
        '''
        tables = query_api.query(query, org=influx_db_server_config["org"])
        return tables.to_json()
    def POST(self, *uri):
        try:
            data_to_insert = cherrypy.request.body.read()
            converted_data = json.loads(data_to_insert)
            print(data_to_insert)
            influx_db_server_config = initialize_influx_connection()
            write_client = influxdb_client.InfluxDBClient(url=influx_db_server_config["url"],
                                                          token=influx_db_server_config["token"],
                                                          org=influx_db_server_config["org"])
            write_api = write_client.write_api(write_options=SYNCHRONOUS)
            point = (
                Point("temprature")
                .tag("user_id", converted_data["user_id"])
                .tag("sensor_id", converted_data["sensor_id"])
                .field("value", converted_data["value"])
            )
            write_api.write(bucket=influx_db_server_config["bucket"], org=influx_db_server_config["org"], record=point)
            return json.dumps({"result": "successful", "operation_successfull": True})
        except Exception as e:
            print(e)
            return json.dumps({"result": "unsuccessful", "operation_successfull": False})

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
    current_service_information = {"service_name": "influx_db_access",
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
            os.environ['IP_PORT'] = "50020"
    except:
        os.environ['IP_PORT'] = "50020"
    try:
        if os.environ['environment'] == None:
            os.environ['environment'] = 'debugging'
    except:
        os.environ['environment'] = 'debugging'
    try:
        if os.environ['INFLUXDB_TOKEN'] == None:
            os.environ[
                'INFLUXDB_TOKEN'] = 'o-nwir-c0VQl8Q7i4w7e30xRKaVCE5ooF5w3s3e1Cpc7tkncQk7OBJpSGVMqGMB0JDq2yGM7SSZaP72XDDcdhw=='
    except:
        os.environ[
            'INFLUXDB_TOKEN'] = 'o-nwir-c0VQl8Q7i4w7e30xRKaVCE5ooF5w3s3e1Cpc7tkncQk7OBJpSGVMqGMB0JDq2yGM7SSZaP72XDDcdhw=='
    try:
        if os.environ['SCD_INFLUXDB_DAL_INFLUXDB_BUCKET'] == None:
            os.environ[
                'SCD_INFLUXDB_DAL_INFLUXDB_BUCKET'] = 'IOT_SCD_PROJECT'
    except:
        os.environ[
            'SCD_INFLUXDB_DAL_INFLUXDB_BUCKET'] = 'IOT_SCD_PROJECT'
    try:
        if os.environ['SCD_INFLUXDB_DAL_INFLUXDB_URL'] == None:
            os.environ[
                'SCD_INFLUXDB_DAL_INFLUXDB_URL'] = 'http://127.0.0.1:8086'
    except:
        os.environ[
            'SCD_INFLUXDB_DAL_INFLUXDB_URL'] = 'http://127.0.0.1:8086'
    try:
        if os.environ['service_catalog'] == None:
            os.environ['service_catalog'] = 'http://127.0.0.1:50010'
    except:
        os.environ['service_catalog'] = 'http://127.0.0.1:50010'
    try:
        if os.environ['SCD_INFLUXDB_DAL_INFLUXDB_URL'] == None:
            os.environ[
                'SCD_INFLUXDB_DAL_ORG'] = 'IOT'
    except:
        os.environ[
            'SCD_INFLUXDB_DAL_ORG'] = 'IOT'
    hearth_influx_db_dal = HeartInfluxDbDal()
    temprature_influx_db_dal = TempratureInfluxDbDal()
    cherrypy_cors.install()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'cors.expose.on': True,
        }
    }

    register_me()

    cherrypy.tree.mount(HeartInfluxDbDal(), '/' + type(HeartInfluxDbDal()).__name__, conf)
    cherrypy.tree.mount(TempratureInfluxDbDal(), '/' + type(TempratureInfluxDbDal()).__name__, conf)
    cherrypy.config.update({'server.socket_host': hearth_influx_db_dal.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(hearth_influx_db_dal.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    #while True:
    #    time.sleep(1)
    cherrypy.engine.block()
