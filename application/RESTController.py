import json

from flask import Flask, request

from application.Service import Service
from application.VirtualMachine import VM

app = Flask(__name__)
service = Service()

@app.route("/vms", methods=["GET"])
def get_list():
    page = request.args.get('page', default = 1, type = int)
    filter = request.args.get('filter', default = '', type = str)
    sort = request.args.get('sort', default = '', type = str)
    vms = get_paginated(filter, sort, page)
    return vms


@app.route("/vms/<id>", methods=["GET"])
def get_vm(id):
    vm = service.get_vm(id)
    if vm is None:
        return '{}'
    return vm.toJSON()


@app.route("/vms", methods=["POST"])
def add_vm():
    data = request.get_json()
    vm = VM()
    vm.create(data)
    service.add_vm(vm)
    return vm.toJSON()


@app.route("/vms/<id>", methods=["PUT"])
def update_vm(id):
    data = request.get_json()
    vm = service.update_vm(id, data)
    return vm.toJSON()


@app.route("/vms/<id>", methods=["DELETE"])
def delete_vm(id):
    return service.remove_vm(id).toJSON()

def get_paginated(filter, sort, page):
    vms = service.get_all_vms(filter, sort, page-1)
    print(len(vms))
    out = json.dumps([ob.__dict__ for ob in vms])
    out = " \"page\": {}," \
          "\"items\": {}".format(page, out)
    out = "{ " + out + " }"
    return out

if __name__ == "__main__":
    for _ in range(15):
        data = {}
        vm = VM()
        vm.create(data)
        service.add_vm(vm)
    app.run()

