#!/usr/bin/env python

from radkit_common.utils.ssl import create_public_ssl_context
from getpass import getpass
from radkit_service.control_api import ControlAPI

from stopwatch import StopWatch

verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)

with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=getpass("Password: "), http_client_kwargs=dict(verify=verify)) as service:
    stopwatch = StopWatch()
    stopwatch.start()
    devices = service.list_devices().get_result()
    stopwatch.stop()
    stopwatch.print_delta("devices listed in ")

    devices_uuid = [device.uuid for device in devices if "test-device-" in device.name]

    print(f"Identified {len(devices_uuid)} devices")

    stopwatch.start()
    service.delete_devices(device_ids=devices_uuid)
    stopwatch.stop()
    stopwatch.print_delta("Devices deleted in ")
