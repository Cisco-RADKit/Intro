#!/usr/bin/env python

from getpass import getpass
from math import floor

from radkit_common.utils.ssl import create_public_ssl_context
from radkit_service.control_api import ControlAPI
from radkit_service.webserver.models.devices import MetaDataEntry, NewDevice, NewTerminal #, StoredDevice
from radkit_common.utils.formatting import to_canonical_name

from stopwatch import StopWatch

password = getpass()
#password = "Cisco123!!!"

verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)

with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=password, http_client_kwargs=dict(verify=verify)) as service:
    stopwatch = StopWatch()

    devices = []
    for i in range(20000):
        hostname = f"new test-device_{i}"
        canonical_name = to_canonical_name(hostname)
        terminal = NewTerminal(
            username="admin",
            password="Cisco123",
        )
        # metadata = [
        #     MetaDataEntry(key="original-hostname", value=hostname),
        #     MetaDataEntry(key="index", value=str(i))
        # ]
        device = NewDevice(
            name=canonical_name,
            host=f"2.{floor(i/(256*256))}.{floor(i/256)}.{i%256}",
            deviceType="IOS",
            terminal=terminal,
            # metaData=metadata,
            enabled=True,
        )
        devices.append(device)

    print(f"creating {len(devices)} devices")
    stopwatch.start()
    result = service.create_devices(devices)
    stopwatch.stop()
    stopwatch.print_delta(f"devices created in ")
