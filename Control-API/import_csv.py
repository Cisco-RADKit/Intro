#!/usr/bin/env python

from getpass import getpass
import csv

from radkit_common.utils.ssl import create_public_ssl_context
from radkit_service.control_api import ControlAPI
from radkit_service.webserver.models.devices import NewDevice

from stopwatch import StopWatch

def read_csv_file(file_path):
    try:
        device_list = []
        with open(file_path, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                name = row['name']
                address = row['address']
                device_type = row['type']
                device_list.append(
                    {
                        'name': name,
                        'address': address,
                        'type': device_type
                    }
                )

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return device_list

# Example usage:
file_path = 'test.csv'
device_list = read_csv_file(file_path)
print(device_list)

password = getpass()

verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)

with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=password, http_client_kwargs=dict(verify=verify)) as service:
    stopwatch = StopWatch()

    devices = []
    for d in device_list:

        device = NewDevice(
            name=d['name'],
            host=d['address'],
            deviceType=d['type'],
            enabled=True,
        )
        devices.append(device)

    print(f"creating {len(devices)} devices")
    stopwatch.start()
    result = service.create_devices(devices)
    stopwatch.stop()
    stopwatch.print_delta(f"Operation completed in ")
    print(f"{result.success_count} devices were created")

    # print failure messages
    for r in result.results:
        if r.__root__.success == False:
            print(f"Could not create {r.__root__.detail['name']}")
            print(r.__root__.message)
            print()
