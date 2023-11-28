# Introduction to RADKit RPC API

Start radkit-client from a shell, your Windows Start menu, Mac Launcher...

All examples shown are from Linux.
```
❯ radkit-client
 ┌─────────────────────────────| RADKit Client - 1.6.0a10+44.g644c310f8 |──────────────────────────────┐
 │                                                                                                     │
 │                  CISCO CONFIDENTIAL -- FOR INTERNAL USE ONLY -- DO NOT DISTRIBUTE                   │
 │                                                                                                     │
 │ Cisco Remote Automation Development Kit (RADKit) -- Copyright (c) 2018-2023 by Cisco Systems, Inc.  │
 │                                                                                                     │
 │ Cisco Online Privacy Statement: <https://www.cisco.com/c/en/us/about/legal/privacy-full.html>       │
 │                                                                                                     │
 │ The use of Cisco RADKit and the associated software and cloud services is governed by the Cisco End │
 │ User License Agreement (EULA) available at:                                                         │
 │ <https://www.cisco.com/c/en/us/about/legal/cloud-and-software/end_user_license_agreement.html>      │
 │                                                                                                     │
 │ For any additional questions regarding the use of this product, please contact `radkit@cisco.com`.  │
 │                                                                                                     │
 │ Certain third-party libraries used by Cisco RADKit are licensed under the GNU Lesser General Public │
 │ License ("LGPL") version 2.1 or version 3, respectively, and come with ABSOLUTELY NO WARRANTY. You  │
 │ can redistribute and/or modify the code for those libraries under the terms of their respective     │
 │ license. For more details, see either: the documentation bundled with Cisco RADKit; the online      │
 │ documentation at <https://radkit.cisco.com/>; or contact `radkit@cisco.com`.                        │
 │                                                                                                     │
 │ For more information about the Open Source components used in this and other Cisco products, please │
 │ refer to the Open Source portal at: <https://www.cisco.com/c/en/us/about/legal.html>                │
 └─────────────────────────────────────────────────────────────────────────────────────────────────────┘
11:11:42.242Z INFO  | internal | CXD object created without authentication set, call `<this object>.authenticate()` to set authentication.
Running startup script(s):
- /<home directory>/.radkit/client/profile.py


Example usage:
    client = sso_login("<email_address>")          # Open new client and authenticate with SSO
    client = certificate_login("<email_address>")  # OR authenticate with a certificate
    client = access_token_login("<access_token>")  # OR authenticate with an SSO Access Token
    service = client.service("<serial>")           # Then connect to a RADKit Service
    service = start_integrated_service()           # Immediately login to an integrated session
    service = direct_login()                       # Establish cloud-less direct connection to service.
    client.grant_service_otp()                     # Enroll a new service

>>>
```

# Logging in

To connect a RADKit Client to the cloud, authentication is required. Here, we will use `sso_login()` to authenticate the user.

```
>>> client = sso_login("<your_cco_id@domain.com>")

A browser window was opened to continue the authentication process. Please follow the instructions there.

Authentication result received.
>>>
```

The API `sso_login("<email address>")` initializes the connection and triggers authentication. It returns an object of type Client. In the example above, we save the return object into a variable names `client`
```
>>> type(client)
<class 'radkit_client.sync.client.Client'>
```


# Connecting to a remote RADKit Service

The Client object has a method called `service()` to trigger the end-to-end connection with a service identified by a Service ID.
```
>>> service = client.service("0pv7-fat8-09b7")
11:18:37.923Z INFO  | internal | Connecting to forwarder [uri='wss://prod.radkit-cloud.cisco.com/forwarder-4/websocket/']
11:18:38.913Z INFO  | internal | Connection to forwarder successful [uri='wss://prod.radkit-cloud.cisco.com/forwarder-4/websocket/']
11:18:39.197Z INFO  | internal | Connecting to forwarder [uri='wss://prod.radkit-cloud.cisco.com/forwarder-1/websocket/']
11:18:39.328Z INFO  | internal | Connection to forwarder successful [uri='wss://prod.radkit-cloud.cisco.com/forwarder-1/websocket/']
>>>
```

The resulting object is of type `Service` and is stored into a variable called `service`
```
>>> type(service)
<class 'radkit_client.sync.service.Service'>
```

# The service inventory DeviceDict

The RADKit Service inventory is a `DeviceDict` (kind of Dict) attribute on the `Service` object:

```
>>> type(service.inventory)
<class 'radkit_client.sync.device.DeviceDict'>
```

`DeviceDict` has a convenient `__repr__` for a default display:

```
>>> print(service.inventory)
<radkit_client.sync.device.DeviceDict object at 0x122d1ab20>
name               host          device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
-----------------  ------------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
cat8kv-1           198.18.1.101  IOS            True        True       False   False      False                  False
iosv-1             198.18.1.11   IOS            True        False      False   False      False                  False
nexus9kv-1         198.18.1.102  NXOS           True        False      False   False      False                  False
radkit             127.0.0.1     RADKitService  True        False      False   True       False                  False
ubuntu-1           198.18.1.100  LINUX          True        False      False   False      False                  False
bad-device         1.1.1.2       LINUX          True        False      True    False      True                   False

Untouched inventory from service 0pv7-fat8-09b7.

```

# Devices

A `DeviceDict` can be indexed by device name; a device name is just a string. A device has a type `Device`.

```
>>> type(service.inventory['ubuntu-1'])
<class 'radkit_client.sync.device.Device'>
```

A `Device` object contains information about a device, and exposes interesting methods we will discover later down.

```
>>> print(service.inventory['ubuntu-1'])
AsyncDevice(name='ubuntu-1', service_display_name='ubuntu-1', host='198.18.1.100', device_type='LINUX', forwarded_tcp_ports='1-65535', failed=False)

Object parameters
--------------------  ------------------
identity              your_cco_id@domain.com
serial                None              
name                  ubuntu-1          
service_display_name  ubuntu-1          
--------------------  ------------------

Internal attributes
key                  value           
-------------------  ------------
description                      
device_type          LINUX       
forwarded_tcp_ports  1-65535     
host                 198.18.1.100
http_config          False       
netconf_config       False       
snmp_config          False       
swagger_config       False       
terminal_config      True        

External attributes

APIs
-------  -------
Netconf  UNKNOWN
Swagger  UNKNOWN
-------  -------
```

Device objects can be assigned to variables too:
```
>>> ubuntu = service.inventory['ubuntu-1']
>>> type(ubuntu)
<class 'radkit_client.sync.device.Device'>
```

# DeviceDict subsets

## Subsets
The method `subset()` on a `DeviceDict` creates a new `DeviceDict` containing only the corresponding items.

```
>>> subdict = service.inventory.subset(["ubuntu-1", "nexus9kv-1"])
>>> print(subdict)
<radkit_client.sync.device.DeviceDict object at 0x10bdee730>
name        host          device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
----------  ------------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
nexus9kv-1  198.18.1.102  NXOS           True        False      False   False      False                  False
ubuntu-1    198.18.1.100  LINUX          True        False      False   False      False                  False

2 device(s) from service 0pv7-fat8-09b7.
>>> type(subdict)
<class 'radkit_client.sync.device.DeviceDict'>
```
## A single device DeviceDict

To create a `DeviceDict` out of a single `Device`, use the `singleton()` method out of the `Device` object.
```
>>> linux = service.inventory['ubuntu-1'].singleton()
>>> print(linux)
<radkit_client.sync.device.DeviceDict object at 0x122fa2f10>
name      host          device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
--------  ------------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
ubuntu-1  198.18.1.100  LINUX          True        False      False   False      False                  False

1 device(s) from service 0pv7-fat8-09b7.
```

This is still a `DeviceDict`:
```
>>> type(linux)
<class 'radkit_client.sync.device.DeviceDict'>
```

## Filters
The method `filter()` on a `DeviceDict` creates a new `DeviceDict` containing only the matched elements.

```
>>> ios = service.inventory.filter("device_type", "IOS")
>>> print(ios)
<radkit_client.sync.device.DeviceDict object at 0x10c199070>
name      host          device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
--------  ------------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
cat8kv-1  198.18.1.101  IOS            True        True       False   False      False                  False
iosv-1    198.18.1.11   IOS            True        False      False   False      False                  False

2 device(s) from service 0pv7-fat8-09b7.
```

A subset of a `DeviceDict` is also a `DeviceDict`:
```
>>> type(ios)
<class 'radkit_client.sync.device.DeviceDict'>
```

## Adding and removing DeviceDict elements

Use the `remove()` method of a `DeviceDict` to remove an item or a series of items.
```
>>> ios.remove('cat8kv-1')
>>> ios
<radkit_client.sync.device.DeviceDict object at 0x122a20f40>
name    host         device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
------  -----------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
iosv-1  198.18.1.11  IOS            True        False      False   False      False                  False

1 device(s) from service 0pv7-fat8-09b7.
```
You can also use a list of strings, a `Device`, or a list of `Device`.

Adding a `Device` in a `DeviceDict` is done with `add()`:
```
>>> ios.add(service.inventory['cat8kv-1'])
>>> print(ios)
<radkit_client.sync.device.DeviceDict object at 0x122a20f40>
name      host          device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
--------  ------------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
cat8kv-1  198.18.1.101  IOS            True        True       False   False      False                  False
iosv-1    198.18.1.11   IOS            True        False      False   False      False                  False

2 device(s) from service 0pv7-fat8-09b7.
```
# Executing CLI commands
`DeviceDict` and `Device` both support an `exec()` method. `exec()` allows you to execute commands on a device, without having to worry about password management, the prompt, multi-page output, etc.

## Executing command on a Device

```
>>> sv = service.inventory['iosv-1'].exec("show version").wait()
```

The `status` field tells you if RADKit could log into the device and execute the command:
```
>>> sv.status
<RequestStatus.SUCCESS: 'SUCCESS'>
```

The output of the command is available in `result.data`:
```
>>> print(sv.result.data)
iosv-1#show version
Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.9(3)M6, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Mon 08-Aug-22 15:22 by mcpre
...
```

## Executing a command on a DeviceDict
A command can be executed on a `DeviceDict`. This will execute the command on all the `Device` in parallel
```
>>> sv = ios.exec("show version").wait()
>>> print(sv.status)
RequestStatus.SUCCESS
```

The results are indexed by `Device` name
```
>>> print(sv.result)
<radkit_client.sync.command.DeviceToSingleCommandOutputDict object at 0x1225991c0>
key       status    identity            service_id      device    device_uuid                           command       data                                                                                              
--------  --------  ------------------  --------------  --------  ------------------------------------  ------------  ----------------------------------------------------------------------------------
cat8kv-1  SUCCESS   your_cco_id@domain.com  0pv7-fat8-09b7  cat8kv-1  5db21d2a-50f1-4477-8f06-8109463d14a7  show version  c8000v#show version\nCisco IOS XE Software, Version 17.09.01a\nCisco IOS Softwa...
iosv-1    SUCCESS   your_cco_id@domain.com  0pv7-fat8-09b7  iosv-1    fed1abaf-268e-49c2-bcff-fdd3dabc2653  show version  iosv-1#show version\nCisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M... 
```

The data extracted from the command is in the `Result`, indexed by device name:
```
>>> print(sv.result['iosv-1'].data)
iosv-1#show version
Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.9(3)M6, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2022 by Cisco Systems, Inc.
Compiled Mon 08-Aug-22 15:22 by mcpre
...
```

## Multiple commands

Multiple commands can be executed in a row on a `Device` or `DeviceDict`. The results are indexed by device (if a `DeviceDict` is used), then by command.

```
>>> show_commands = ios.exec(["show version" , "show ip route"]).wait()
>>> print(show_commands.result['iosv-1']['show ip route'].data)
iosv-1#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
...
```

# Dealing with errors

RADKit only deals with one type of error: the inability to connect to a device with the chosen protocol. This could be cause by the device being shut down, the IP address or port being unreachable, the credentials may be incorrect, ... If anything prevents RADKit from obtaining data, this will result in an errror.


## Failing Device requests
```
>>> ls_output = service.inventory['bad-device'].exec("ls -la").wait()
15:47:55.965Z ERROR | internal | command execution failed [device_name='bad-device' commands=['ls -la'] error="Device action failed: Connection error while preparing connection. Reason: Failed after the configured number of attempts. Last error: [Errno 111] Connect call failed ('1.1.1.1', 22). Attempts=1. Connection timeout=30.0s. Backoff time=2.0s.."]
```

The error log is useful to a human user watching the terminal. To programatically verify the status, use the result's `status` field
```
>>> ls_output.result.status
<ExecResultStatus.FAILURE: 'FAILURE'>
```

The status is an enum of type `ExecResultStatus`, but it also translates into a string.

When a request has faile, the result data is unset and raises an exception if one tries to address it
```
>>> ls_output.result.data
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../sync/from_async/autowrap.py", line 252, in __get__
    return self.func(obj)
...
    self._exception_func()
  File ".../async_/command.py", line 276, in raise_
    raise ExecFailedError("command execution failed: %s" % error.error_message)
radkit_client.async_.command.ExecFailedError: command execution failed: Device action failed: Connection error while preparing connection. Reason: OS error: No route to host [bad-device@1.1.1.2:22].
```

## Failing multi-command and DeviceDict requests

Let's first create a `DeviceDict` with a failing device:
```
>>> ios = service.inventory.subset(["cat8kv-1", "iosv-1", "bad-device"])
>>> ios
<radkit_client.sync.device.DeviceDict object at 0x12665b8e0>
name        host          device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
----------  ------------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
bad-device  1.1.1.2       LINUX          True        False      True    False      True                   True 
cat8kv-1    198.18.1.101  IOS            True        True       False   False      False                  False
iosv-1      198.18.1.11   IOS            True        False      False   False      False                  False

3 device(s) from service 0pv7-fat8-09b7.
```

```
>>> show_ver = ios.exec("show version").wait()
07:06:23.678Z ERROR | internal | command execution failed [device_name='bad-device' commands=['show version'] error='Device action failed: Connection error while preparing connection. Reason: OS error: No route to host [bad-device@1.1.1.2:22].']
```

Notice the request status is `PARTIAL_SUCCESS` as some devices respondes, while others did not
```
>>> show_ver
[PARTIAL_SUCCESS] <radkit_client.sync.request.TransformedFillerRequest object at 0x13003e850>
----------------  --------------------------------------------------------------------------------
sent_timestamp    2023-11-22 08:06:22                                                             
request_type      Command execution                                                               
client_id         your_cco_id@domain.com                                                              
service_id        0pv7-fat8-09b7                                                                  
updates           3 total, 2 succeeded, 1 failed                                                  
result            {'iosv-1': AsyncExecSingleCommandResult(command='show version', status='SUCCE...
forwarder         wss://prod.radkit-cloud.cisco.com/forwarder-1/                                  
e2ee_used         True                                                                            
compression_used  zstd                                                                            
----------------  --------------------------------------------------------------------------------

>>> show_ver.status
<RequestStatus.PARTIAL_SUCCESS: 'PARTIAL_SUCCESS'>
```

Individual device result status is also available
```
>>> show_ver.result
<radkit_client.sync.command.DeviceToSingleCommandOutputDict object at 0x127d71be0>
key         status    identity            service_id      device      device_uuid                           command       data                                                                                                                                                                                       
----------  --------  ------------------  --------------  ----------  ------------------------------------  ------------  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bad-device  FAILURE   your_cco_id@domain.com  0pv7-fat8-09b7  bad-device  ef9058fc-8b66-4d2e-8cdd-bd01915754ae  show version  ExecFailedError('command execution failed: Device action failed: Connection error while preparing connection. Reason: OS error: No route to host [bad-device@1.1.1.2:22].')
cat8kv-1    SUCCESS   your_cco_id@domain.com  0pv7-fat8-09b7  cat8kv-1    5db21d2a-50f1-4477-8f06-8109463d14a7  show version  c8000v#show version\nCisco IOS XE Software, Version 17.09.01a\nCisco IOS Softwa...                                                                                         
iosv-1      SUCCESS   your_cco_id@domain.com  0pv7-fat8-09b7  iosv-1      fed1abaf-268e-49c2-bcff-fdd3dabc2653  show version  iosv-1#show version\nCisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M...                                                                                          

>>> show_ver.result['iosv-1'].status
<ExecResultStatus.SUCCESS: 'SUCCESS'>

>>> show_ver.result['bad-device'].status
<ExecResultStatus.FAILURE: 'FAILURE'>
```

# Integration task

Let's put everything together now. Here is a small exercise; the solution is below.

* Create a list of devices containig `bad-device`, `cat8kv-1`, and `iosv-1`.
* execute the command `show version` on those devices
* print the name of each device, along with its version
* cater for errors; do not crash
 
```
>>> import regex as re

>>> # import ExecResultStatus from the radkit_client library to verify status
>>> from radkit_client import ExecResultStatus

>>> version_regex = re.compile("Version\s+(\S+),", flags=re.DOTALL)
>>> for name, device_result in show_ver.result.items():
      if device_result.status != ExecResultStatus.SUCCESS:
        print(f"no response from {name}")
        continue
    version = version_regex.findall(device_result.data)[0]
    print(f"{name} -> {version}")
```

This results in the following output
```
iosv-1 -> 15.9(3)M6
cat8kv-1 -> 17.9.1a
no response from bad-device
>>>
```
