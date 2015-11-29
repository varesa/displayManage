import os
import json

import app.vars


class DevicesWrapper:
    def __init__(self):
        pass

    def get(self) -> list:
        if not os.path.isfile(app.vars.devicespath):
            self.write([])
        with open(app.vars.devicespath, "r") as devicesfile:
            return json.load(devicesfile)

    def write(self, data: list) -> None:
        if not os.path.exists(app.vars.datapath):
            os.mkdir(app.vars.datapath)
        with open(app.vars.devicespath, "w") as devicesfile:
            json.dump(data, devicesfile)
