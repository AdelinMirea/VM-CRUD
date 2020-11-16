from application.Persistence import Persistence


class Service:
    def __init__(self):
        self._persistence = Persistence()

    def get_all_vms(self, filter, sort, page):
        filters_ = filter.split(",")
        filters = []
        for filter in filters_:
            if len(filter.split(":")) == 2:
                filters.append((filter.split(":")[0], filter.split(":")[1]))

        vms = self._persistence.get_all()
        vms = self.filter(vms, filters)
        vms = self.sort(vms, sort)
        vms = self.paginate(vms, page)
        return vms

    def get_vm(self, id):
        id = int(id)
        return self._persistence.get_by_id(id)

    def add_vm(self, vm):
        self._persistence.add(vm)

    def update_vm(self, id, data):
        id = int(id)
        vm = self.generate_vm(self._persistence.get_by_id(id), data)
        self._persistence.add(vm)
        return vm

    def remove_vm(self, id):
        id = int(id)
        return self._persistence.remove(id)

    def generate_vm(self, old, new_json):
        return old.update(new_json)

    def filter(self, vms, filters):
        final = []
        for vm in vms:
            add_in_final = True
            for (field, match) in filters:
                if field == "cpu":
                    add_in_final = add_in_final and (match in vm.cpu)
                elif field == "memory":
                    add_in_final = add_in_final and (match in vm.memory)
                elif field == "persistent_storage":
                    add_in_final = add_in_final and (match in vm.persistent_storage)
                elif field == "tag":
                    add_in_final = add_in_final and (match in vm.tags)
                elif field == "region":
                    add_in_final = add_in_final and (match in vm.region)
                elif field == "state":
                    add_in_final = add_in_final and (match in vm.state)
                elif field == "group":
                    add_in_final = add_in_final and (match in vm.group)
            if add_in_final:
                final.append(vm)

        return final

    def sort(self, vms, sort):
        if len(sort.split(":")) != 2:
            return vms

        field = sort.split(":")[0]
        descendent = sort.split(":")[1].lower() != 'asc'

        if field == "cpu":
            vms.sort(key=lambda x: x.cpu, reverse=descendent)
        elif field == "memory":
            vms.sort(key=lambda x: x.memory, reverse=descendent)
        elif field == "persistent_storage":
            vms.sort(key=lambda x: x.persistent_storage, reverse=descendent)
        elif field == "region":
            vms.sort(key=lambda x: x.region, reverse=descendent)
        elif field == "state":
            vms.sort(key=lambda x: x.state, reverse=descendent)
        elif field == "group":
            vms.sort(key=lambda x: x.group, reverse=descendent)

        return vms

    def paginate(self, vms, page):
        page = int(page)
        if page < 0:
            return vms

        start = 10 * (page)

        return vms[start:start+10]