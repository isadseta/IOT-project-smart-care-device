import json
import os
import datetime
import time
import requests

class Service():
    def __init__(self, service_name=None, ip_address=None, ip_port=None):
        if service_name is None:
            self.service_name = os.environ['SERVICE_NAME']
        else:
            self.service_name = service_name

        if ip_address is None:
            self.ip_address = os.environ['IP_ADDRESS']
        else:
            self.ip_address = ip_address

        if ip_port is None:
            self.ip_port = os.environ['IP_PORT']
        else:
            self.ip_port = service_name
        self.url = self.create_url()

    def create_url(self):
        url = "http://" + self.ip_address + ":" + str(self.ip_port) + "/" + self.service_name
        return url

    def jsonify(self):
        service = {'IP_address': self.ip_address, 'port': self.ip_port, 'service': '/' + self.service_name,
                   'url': self.url}
        return service


class BaseService(object):
    last_config_load = datetime.datetime.now() - datetime.timedelta(minutes=2)

    def __init__(self):
        self.serviceCatalogIP = os.environ['IP_ADDRESS']
        self.serviceCatalogPort = os.environ['IP_PORT']
        self.serviceCatalogIP = os.environ['IP_ADDRESS']
        self.serviceCatalogPort = os.environ['IP_PORT']
        self.last_config_load = datetime.datetime.now() - datetime.timedelta(minutes=2)

    def reload_config(self):
        global system_config
        # getting system configs
        service_catalog_address = os.environ['service_catalog'] + "/ServiceCatalog/summary"
        while True:
            try:
                system_config = requests.get(service_catalog_address)
                print("==================================================================================")
                print("Configuration loaded successfully.")
                print(system_config)
                break
            except Exception as ex:
                print("==================================================================================")
                print(f"Unsucceessfull loading cofiguration because of \n {ex}.")
                time.sleep(5)

    def system_config(self):
        global system_config
        current_time = datetime.datetime.now()
        time_difference = current_time - self.last_config_load
        minutes_difference = time_difference.total_seconds() / 60
        if minutes_difference > 1 or system_config is None:
            self.reload_config()
        system_config_as_cixtionary = {}
        for service_item in system_config.json():
            print(service_item)
            system_config_as_cixtionary[service_item["service_name"]] = service_item
        print(system_config_as_cixtionary)
        return system_config_as_cixtionary