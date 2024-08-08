#!/usr/bin/env python

from getpass import getpass
from math import floor

from radkit_common.utils.ssl import create_public_ssl_context
from radkit_service.control_api import ControlAPI
from radkit_service.webserver.models.devices import MetaDataEntry, NewDevice, NewTerminal #, StoredDevice

from stopwatch import StopWatch

password = getpass()

verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)

with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=password, http_client_kwargs=dict(verify=verify)) as service:
    stopwatch = StopWatch()

    devices = []
    for i in range(10):
        hostname = f"new-test-device-{i}"
        terminal = NewTerminal(
            username="admin",
            password="Cisco123",
        )

        device = NewDevice(
            name=hostname,
            host=f"10.0.{floor(i/254)}.{i%254+1}",
            deviceType="IOS",
            terminal=terminal,
            enabled=True,
        )
        devices.append(device)

    print(f"creating {len(devices)} devices")
    stopwatch.start()
    result = service.create_devices(devices)
    stopwatch.stop()
    stopwatch.print_delta(f"Operation completed in ")
    print(f"{result.success_count} devices were created")
