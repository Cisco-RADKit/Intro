#!/usr/bin/env python

from getpass import getpass

from radkit_common.utils.ssl import create_public_ssl_context
from radkit_service.control_api import ControlAPI
from radkit_service.webserver.models.devices import UpdateDevice

from time import time
from stopwatch import StopWatch

verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)
with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=getpass("Password: "), http_client_kwargs=dict(verify=verify)) as service:
    stopwatch = StopWatch()
    print("Getting device list")
    stopwatch.start()
    devices = service.list_devices().get_result()
    stopwatch.stop()
    stopwatch.print_delta("devices listed in ")

    devices = [device for device in devices if "test-device-" in device.name]

    print(f"Identified {len(devices)} devices")

    now = time()
    new_description = f"modified {now}"
    for i in range(len(devices)):
        devices[i].description = new_description
        devices[i].name = "new-test-device-1"

    print("Sending to RADKit Service")
    stopwatch.start()
    result = service.update_devices(devices)
    stopwatch.stop()
    stopwatch.print_delta(f"Operation completed in ")

    if result.success != True:
        for r in result.results:
            if r.__root__.success == False:
                print(f"{r.__root__.detail['name']} could not be modified: {r.__root__.message}")
                print()
