import json
import os

import app.vars


class MatrixWrapper:
    def __init__(self):
        pass

    def get(self) -> dict:
        if not os.path.isfile(app.vars.matrixpath):
            self.write({})
            
        with open(app.vars.matrixpath, "r") as matrixfile:
            return json.load(matrixfile)

    def write(self, data: dict) -> None:
        if not os.path.exists(app.vars.datapath):
            os.mkdir(app.vars.datapath)
        with open(app.vars.matrixpath, "w") as matrixfile:
            json.dump(data, matrixfile)