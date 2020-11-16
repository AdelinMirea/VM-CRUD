import json
from os.path import expanduser

from application.VirtualMachine import VM


class FilePersistence:

    def __init__(self):
        home = expanduser("~")
        self._file_name = home + "/vms.json"

    def read(self):
        items = []
        with open(self._file_name, 'r') as file:
            for line in file.readlines():
                vm = VM()
                props = json.loads(line)
                vm.create(props)
                items.append(vm)

        return items

    def write(self, data):
        with open(self._file_name, 'w') as file:
            for item in data:
                out = item.toJSON()
                file.write(out)
                file.write("\n")
