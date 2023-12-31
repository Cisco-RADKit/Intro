# Introduction to RADKit Control API

## Preamble
RADKit Service offers a Web UI to manage RADKit Service. From the WebUI, an administrator can control the inventory (add, remove, modify devices), remote user access (manage users, role-based access control, ...) and many more administrative tasks.

The Web UI is built on top of a REST API, which is wrapped into a Python API. For this reason, the whole set of APIs to control RADKit Service is aptly named the RADKit Control API (or simply the Control API for short).

The Control API is only available "locally", i.e. the process calling the Control API must have direct API connectivity to the RADKit Service. The Control API is also gated by administrator credentials: the API client must authenticate using adminstrator (including superadmin) credentials.

It is possible to expose the Control API to remote users, but this is out of the scope of this introduction.

:warning: In this document, we will use object names Service, Device, ... The names are the same as the RPC equivalent object as they represent the same underlying entity. It is important to realize however that the methods available on the Control API objects are completely different from the equivalen RPC API objects. The Control API objects are meant to manage the RADKit Service, while the RPC API objects are meant to query the physical devices.

## Admin credentials

:warning: it is **VERY BAD SECURITY PRACTICE** to store passwords in your scripts and automations. One mistake, and those passwords end up in a public GIT repository, or on an online backup, for any attacker to harvest.

We will instead request the user to provide the administrator password
```python
from getpass import getpass
password = getpass("superadmin password: ")
```


## Connecting to a RADKit Service Control API

The first thing to do is to create a Python context offering an authenticated connection to RADKit Service.

For the purpose of this exercise, we need a RADKit Service - you can create one on your own computer; it will be accessible on `localhost:8081`. Since this vanilla RADKit Service is likely fitted with default self-signed certificates, certificate validation must be omitted.

We can achieve that by creating an ssl context using `create_public_ssl_context()`, which we need to import first:
```python
from radkit_common.utils.ssl import create_public_ssl_context
```

Let's define a `verify` variable from `create_public_ssl_context`:
```python
verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)
```

We need a ControlAPIcontext, let's import it first
```python
from radkit_service.control_api import ControlAPI
```

And now let's create a context called `service`using the `ControlAPI` in a context manager construct:
```python
with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=password, http_client_kwargs=dict(verify=verify)) as service:
```

The above context will authenticate as `superadmin` on the RADKit service running on your local computer (`localhost`).

## Create a device object in memory
Now let's create a device representation in memory (object). From a Control API standpoint, a device is a JSON object. However, RADKit offers pydantic equivalent, allowing you to code more efficiently, and safely.

If you are unfamiliar with Pydantic, visit https://pydantic.dev.

In a nutshell, Pydantic offers Python object representations similar to a Python Data Classes or a C struct. In addition, at creation time, Pydantic will validate and make sure the data matches the expected format for each field.

For this, we need to import the Device models:
```python
from radkit_service.webserver.models.devices import NewDevice
```

```python
  device = NewDevice(
    name="new-device",
    host="10.0.0.1",
    deviceType="IOS",
    enabled=True,
  )
```

One can easily recognize the various parameters of the NewDevice object, and map them to the Web UI options in the RADKit Service Web UI.

## Create the device on RADKit Service

To create the device on RADKit Service, use the `create_device()` member function from the `service` object:
```python
  result = service.create_device(device)
```

:warning: the API `create_device()` creates a single device. To create multiple devices in bulk, use `create_devices()` (plural) as it is thousands of times more efficient than calling `create_device()` multiple times.

Now connect to the RADKit Service using `radkit-client` or `radkit-network-console`. `new-device` should be part of the inventory.

## Device and protocols

The device we created above is not terribly useful as it has no defined protocol to collect data. Let's create a new device, this time with SSH and REST APIs.

We need to define terminal and HTTP-based API parameters; this is done with the `NewTerminal` and `NewHTTP` objects. Let's import their definition:
```python
from radkit_service.webserver.models.devices import NewTerminal, NewHTTP
```

Define terminal parameters:
```python
  terminal = NewTerminal(
    username="admin",
    password="Cisco123",
  )
```

Define HTTP parameters:
```python
  http = NewHTTP(
    username="admin",
    password="Cisco123",
    verify=False, # do not very the device certificate (self-signed)
  )
```

Again, the parameters are the same as those exposed in the WebUI.

We can create a `NewDevice` object, and attach the `NewTerminal` and `NewHTTP` objects to it:

```python
  device_ssh_rest = NewDevice(
    name="new-device-2",
    host="10.0.0.2",
    deviceType="IOS",
    enabled=True,
    terminal=terminal,
    http=http,
  )
```
Finally, the device can be created:
```python
    result = service.create_device(device_ssh_rest)
```

## Creating multiple devices

To create multiple devices, create a list of `NewDevice` and use the `create_devices()` method from the `service` context.

```python
device_list = []

for i in range(10):
    device = NewDevice(
    name=f"new-device-{i}",
    host=f"10.0.0.{i+1}",
    deviceType="IOS",
    enabled=True,
    )
    device_list.append(device)

result = service.create_devices(device_list)
```

# Analyzing results

:warning: While we have stabilized the API for creating and modifying users or devices, the result codes and status require work, cleanup and modification. Expect changes in the result parsing in the next releases. Monitor the Release Notes as this will be advertised in "Breaking Changes".

The result from `create_device()` contains several interesting elements:

`result.success` is `False` if any device cannot be created:
```python
>>> result.success
True
```

`result.success_count` gives a count of how many devices have been actually created.
```python
>>> result.success_count
10
```

When devices are created they get assigned a UUID (an internal unique identifier) by RADKit Service. The status of each device is in `result.results`which is an array with one entry per device:

```python
>>> result.results[0].__root__.dict()
{'success': True, 'result': {'uuid': UUID('7a1c3ad9-9ff1-4faa-bcc5-815f828d62d4'), 'name': 'new-device-0', 'host': '10.0.0.1', 'deviceType': <DeviceType.IOS: 'IOS'>, 'description': '', 'labels': frozenset(), 'jumphostUuid': None, 'sourceKey': None, 'sourceDevUuid': None, 'metaData': [], 'enabled': True, 'terminal': None, 'netconf': None, 'snmp': None, 'swagger': None, 'http': None, 'forwardedTcpPorts': ''}}
>>> result.results[9].__root__.success
True
>>> result.results[9].__root__.result.uuid
UUID("7a1c3ad9-9ff1-4faa-bcc5-815f828d62d4")
```

In case of failure, `success`would be false for the specific device, and the message string would contain the reason for failure of that specific device:
```python
>>> result.success
False
>>> result.results[0].__root__.dict()
{
    "success": False,
    "message": '1 validation error for Device name "new-device-5" already exists\nname\n  Device name "new-device-5" already exists [type=value_error, input_value=\'\', input_type=str]',
    "detail": {"uuid": None, "name": "new-device-5", "host": "10.0.0.10", "deviceType": "IOS"},
}
>>> result.results[0].__root__.message
'1 validation error for Device name "new-device-0" already exists\nname\n  Device name "new-device-0" already exists [type=value_error, input_value=\'\', input_type=str]'
```

## Putting it all together

See `create_devices.py`and other examples in this directory.

```python
#!/usr/bin/env python

from getpass import getpass
from math import floor

from radkit_common.utils.ssl import create_public_ssl_context
from radkit_service.control_api import ControlAPI
from radkit_service.webserver.models.devices import MetaDataEntry, NewDevice, NewTerminal #, StoredDevice
from radkit_common.utils.formatting import to_canonical_name

password = getpass()

verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)

with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=password, http_client_kwargs=dict(verify=verify)) as service:

    # create an empty device list
    devices = []
    for i in range(10):
        # create an in-memory device
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
        # add the device to the list
        devices.append(device)

    print(f"creating {len(devices)} devices")
    result = service.create_devices(devices)

    print(f"{result.success_count} devices were created")

    # print failure messages
    for r in result.results:
        if r.__root__.success == False:
            print(f"Could not create {r.__root__.detail['name']}")
            print(r.__root__.message)
            print()
```
