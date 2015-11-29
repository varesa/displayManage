from pyramid.view import view_config

from app.devicesWrapper import DevicesWrapper


@view_config(route_name='devices', renderer="templates/devices.pt")
def view_devices(request):
    devices = DevicesWrapper().get()
    if "action" in request.POST.keys():
        if request.POST['action'] == "create":
            name = request.POST['name']
            if len(name) and name not in devices:
                devices.append(name)
                DevicesWrapper().write(devices)
        elif request.POST['action'] == "remove":
            for key in request.POST.keys():
                if key.startswith("cb-"):
                    name = key[3:]
                    if name in devices:
                        devices.remove(name)
            DevicesWrapper().write(devices)
    if False:
        pass
    else:
        newdata = DevicesWrapper().get()
    return {"devices": sorted(newdata)}
