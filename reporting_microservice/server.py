import threading

import cherrypy
import json
import requests
import time
import sys
import os
import cherrypy_cors
from utilities.service_class import BaseService, system_config
import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime, timedelta
def cors_tool():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"


cherrypy.tools.cors = cherrypy.Tool('before_handler', cors_tool)
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
            analyze_meaturments= True
            try:
                resource_catalog=app_config["resource_catalog"]["service_value"]
                resource_catalog=resource_catalog + f"/UsersManagerService?id={user_id}"
                user_data=requests.get(resource_catalog).json()[0]
                minimum_heart_rate = user_data["min_heart_rate"]
                maximum_heart_rate = user_data["max_heart_rate"]
                minimum_body_temprature_rate = user_data["min_body_temprature"]
                maximum_body_temprature_rate = user_data["max_body_temprature"]
                if minimum_heart_rate == None or maximum_heart_rate == None or minimum_body_temprature_rate == None or maximum_body_temprature_rate == None:
                    analyze_meaturments = False
            except:
                analyze_meaturments = False

            senser_id_prefix=params["senser_id_prefix"]
            date_days_length=params["date_days_length"]
            influx_db_access_url=app_config["influx_db_access"]["service_value"]
            reporting_parameter=uri[0]
            if reporting_parameter=='heart':
                reporting_url=influx_db_access_url+f'/HeartInfluxDbDal?user_id={user_id}&senser_id_prefix={senser_id_prefix}&date_days_length={date_days_length}'
                report_result=requests.get(reporting_url).json()
                for item in report_result:
                    if analyze_meaturments:
                        if float(item["_value"])<float(minimum_heart_rate) or float(item["_value"])>float(maximum_heart_rate)  :
                            item["analyze"]="Bad"
                        else:
                            item["analyze"] = "Good"
                    else:
                        item["analyze"] = "not_analyzed"
                return json.dumps(report_result)

            if reporting_parameter=='temprature':
                reporting_url=influx_db_access_url+f'/TempratureInfluxDbDal?user_id={user_id}&senser_id_prefix={senser_id_prefix}&date_days_length={date_days_length}'
                report_result=requests.get(reporting_url).json()
                for item in report_result:
                    if analyze_meaturments:
                        if float(item["_value"])<float(minimum_body_temprature_rate) or float(item["_value"])>float(maximum_body_temprature_rate):
                            item["analyze"]="Bad"
                        else:
                            item["analyze"] = "Good"
                    else:
                        item["analyze"] = "not_analyzed"
                return json.dumps(report_result)
        except Exception as ex:
            raise Exception(ex)
        return 'not found report with these parametere'



    def POST(self, *uri):
        pass

    def PUT(self, *uri):
        pass

    def DELETE(self, *uri):
        pass


@cherrypy.tools.cors()
class MockSampleHeartChart():
    exposed = True

    def __init__(self):
        self.catalog = BaseService()
    @cherrypy.tools.cors()
    def GET(self, *uri):
        # Generate heart rate data for the last 1 hour
        time_points, heart_rate_data = self.generate_heart_rate_data()

        # Create a plot of the heart rate data
        fig, ax = plt.subplots()
        ax.plot(time_points, heart_rate_data, color='red', marker='o')

        # Formatting the plot
        ax.set_title("Heart Rate Over the Last Hour")
        ax.set_xlabel("Time (minutes ago)")
        ax.set_ylabel("Heart Rate (bpm)")
        ax.grid(True)

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45, ha="right")

        # Save the image to a bytes buffer
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)

        # Close the plot to avoid memory leaks
        plt.close()

        # Set the content type to image/png
        cherrypy.response.headers['Content-Type'] = 'image/png'

        # Return the image data
        return img_bytes.getvalue()
    def generate_heart_rate_data(self):
        # Simulate heart rate data over the last hour (data every minute)
        current_time = datetime.now()
        time_points = [current_time - timedelta(minutes=i) for i in range(60)]
        time_points.reverse()

        # Generate some random heart rate data between 60 and 100 bpm
        heart_rate_data = np.random.randint(60, 100, size=60)

        # Format the time points as "MM:SS"
        time_points_formatted = [t.strftime("%H:%M") for t in time_points]

        return time_points_formatted, heart_rate_data
    @cherrypy.tools.cors()
    def OPTIONS(self, *args, **kwargs):
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return ''
@cherrypy.tools.cors()
class MockSampleBodyTemprature():
    exposed = True

    def __init__(self):
        self.catalog = BaseService()
    @cherrypy.tools.cors()
    def GET(self, *uri):
        # Generate body temperature data for the last 1 hour
        time_points, temp_data = self.generate_temperature_data()

        # Create a plot of the temperature data
        fig, ax = plt.subplots()
        ax.plot(time_points, temp_data, color='blue', marker='o')

        # Formatting the plot
        ax.set_title("Body Temperature Over the Last Hour")
        ax.set_xlabel("Time (minutes ago)")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True)

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45, ha="right")

        # Save the image to a bytes buffer
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)

        # Close the plot to avoid memory leaks
        plt.close()

        # Set the content type to image/png
        cherrypy.response.headers['Content-Type'] = 'image/png'

        # Return the image data
        return img_bytes.getvalue()

    def generate_temperature_data(self):
        # Simulate body temperature data over the last hour (data every minute)
        current_time = datetime.now()
        time_points = [current_time - timedelta(minutes=i) for i in range(60)]
        time_points.reverse()

        # Generate some random body temperature data between 36.5 and 37.5°C
        temp_data = np.random.uniform(36.5, 37.5, size=60)

        # Format the time points as "HH:MM"
        time_points_formatted = [t.strftime("%H:%M") for t in time_points]

        return time_points_formatted, temp_data
    @cherrypy.tools.cors()
    def OPTIONS(self, *args, **kwargs):
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return ''

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

    cherrypy.tools.cors = cherrypy.Tool('before_handler', cors_tool)
    relational_database_dal_service = MeaturmentsMicroservice()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(MockSampleHeartChart(), '/' + type(MockSampleHeartChart()).__name__, conf)

    cherrypy.tree.mount(MockSampleBodyTemprature(), '/' + type(MockSampleBodyTemprature()).__name__, conf)

    cherrypy.tree.mount(MeaturmentsMicroservice(), '/' + type(MeaturmentsMicroservice()).__name__, conf)
    cherrypy.config.update({'server.socket_host': relational_database_dal_service.catalog.serviceCatalogIP})
    cherrypy.config.update({'server.socket_port': int(relational_database_dal_service.catalog.serviceCatalogPort)})
    cherrypy.engine.start()
    while True:
        time.sleep(1)
    cherrypy.engine.block()
