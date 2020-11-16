from FilePersistence import FilePersistence


class Persistence:
    def __init__(self):
        self._file_persistence = FilePersistence()
        self._vms = {}
        for item in self._file_persistence.read():
            self._vms[item.id] = item

    def get_all(self):
        return self._vms.values()

    def get_by_id(self, id):
        if id in self._vms.keys():
            return self._vms[id]
        return None

    def add(self, vm):
        self._vms[vm.id] = vm
        self._file_persistence.write(self._vms.values())

    def remove(self, id):
        obj = self._remove(id)
        self._file_persistence.write(self._vms.values() )
        return obj

    def _remove(self, id):
        if id in self._vms.keys():
            value = self._vms[id]
            del self._vms[id]
            return value
        return None

    def get_next_id(self):
        if len(self._vms.keys()) == 0:
            return 1
        return max(self._vms.keys()) + 1
