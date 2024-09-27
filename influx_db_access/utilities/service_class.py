import json
import os

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
    def __init__(self):
        self.serviceIP = os.environ['IP_ADDRESS']
        self.servicePort = os.environ['IP_PORT']