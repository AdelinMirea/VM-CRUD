import datetime
import json
import threading
from time import sleep



class VM:

    def __init__(self, id=-1):
        self.id = id
        self.cpu = ""
        self.memory = ""
        self.persistent_storage = ""
        self.ip = ""
        self.public_key = ""
        self.private_key = ""
        self.temporary_storage = ""
        self.state = ""  # stopped, hibernated
        self.region = ""
        self.tags = []
        self.group = ""
        self.up_time = 0
        self.start_time = str(datetime.datetime.now())
        self.created = str(datetime.datetime.now())

        # firewall
        self.open_ports = []
        self.allowed_ip_from_groups = []  #

    def reboot(self):
        if self.state == "ON":
            self.start_time = str(datetime.datetime.now())
            self.temporary_storage = 0
            self.state = "REBOOTING"
            thread = threading.Thread(target=self.power_after_reboot)
            thread.start()

    def power_after_reboot(self):
        sleep(10)
        self.state = "ON"

    def turn_on(self):
        if self.state == "OFF":
            self.start_time = str(datetime.datetime.now())
            self.state = "ON"

    def turn_off(self):
        if self.state != "REBOOT":
            self.state = "OFF"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

    def create(self, data):
        self.id = get_value(data, 'id')
        if self.id == '':
            self.id = get_next_id()

        self.cpu = get_value(data, 'cpu', "Intel i3")
        self.memory = get_value(data, 'memory', '1 GB')
        self.persistent_storage = get_value(data, 'persistent_storage', "1 GB")
        self.ip = get_value(data, 'ip', "127.0.0.1")
        self.public_key = get_value(data, 'public_key')
        self.private_key = get_value(data, 'private_key')
        self.temporary_storage = get_value(data, 'temporary_storage')
        self.state = get_value(data, 'state', "ON")
        self.region = get_value(data, 'region', "USA West")
        self.tags = get_value(data, 'tags', list())
        self.group = get_value(data, 'group')
        self.up_time = get_value(data, 'up_time', "0")
        self.start_time = get_value(data, 'start_time', str(datetime.datetime.now()))
        self.created = get_value(data, 'created', str(datetime.datetime.now()))

        self.open_ports = get_value(data, 'open_ports', list())
        self.allowed_ip_from_groups = get_value(data, 'allowed_ip_from_groups', list())
        return self

    def update(self, new_json: dict):
        self.cpu = get_value(new_json, 'cpu', self.cpu)
        self.memory = get_value(new_json, 'memory', self.memory)
        self.persistent_storage = get_value(new_json, 'persistent_storage', self.persistent_storage)
        self.ip = get_value(new_json, 'ip', self.ip)
        self.public_key = get_value(new_json, self.public_key)
        self.private_key = get_value(new_json, self.private_key)
        self.temporary_storage = get_value(new_json, self.temporary_storage)
        self.state = get_value(new_json, 'state', self.state)
        self.region = get_value(new_json, 'region', self.region)
        self.tags = get_value(new_json, 'tags', self.tags)
        self.group = get_value(new_json, 'group', self.group)
        self.up_time = get_value(new_json, 'up_time', self.up_time)
        self.start_time = get_value(new_json, 'start_time', self.start_time)
        self.created = get_value(new_json, 'created', self.created)

        self.open_ports = get_value(new_json, 'open_ports', self.open_ports)
        self.allowed_ip_from_groups = get_value(new_json, 'allowed_ip_from_groups', self.allowed_ip_from_groups)

        return self


def get_value(dict, key, default=""):
    if key in dict.keys() and dict[key] != '':
        return dict[key]
    return default
