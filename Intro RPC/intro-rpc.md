# Introduction to RADKit RPC API

Start radkit-client from a shell, your Windows start menu, Mac Launcher...

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
- /Users/fdetienn/.radkit/client/profile.py


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

# Loggin in

To connect a RADKit Client to the cloud, authentication is required. Here, we will use `sso_login()` to authenticate the user.

```
>>> client = sso_login("fdetienn@cisco.com")

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

# Manipulate the service inventory

The RADKit Service inventory is a `DeviceDict` (kind of Dict) attribute on the `Service` object:

```
>>> type(service.inventory)
<class 'radkit_client.sync.device.DeviceDict'>
```

`DeviceDict` has a convenient `__repr__` for a default display:

```
>>> print(service.inventory)
<radkit_client.sync.device.DeviceDict object at 0x10bd622e0>
name        host          device_type    Terminal    Netconf    SNMP    Swagger    HTTP    description    failed                   
----------  ------------  -------------  ----------  ---------  ------  ---------  ------  -------------  --------
cat8kv-1    198.18.1.101  IOS            True        True       False   False      False                  False
iosv-1      198.18.1.11   IOS            True        False      False   False      False                  False
nexus9kv-1  198.18.1.102  NXOS           True        False      False   False      False                  False
radkit      127.0.0.1     RADKitService  True        False      False   True       False                  False
ubuntu-1    198.18.1.100  LINUX          True        False      False   False      False                  False

Untouched inventory from service 0pv7-fat8-09b7.
```

## Accessing Devices from a DeviceDict

A `DeviceDict` can be indexed by device name; a device name is just a string. A device has a type Device.

```
>>> type(service.inventory['ubuntu-1'])
<class 'radkit_client.sync.device.Device'>
```

A `Device` object contains information about a device, and exposes interesting methods we will discover in a little moment.

```
>>> print(service.inventory['ubuntu-1'])
AsyncDevice(name='ubuntu-1', service_display_name='ubuntu-1', host='198.18.1.100', device_type='LINUX', forwarded_tcp_ports='1-65535', failed=False)

Object parameters
--------------------  ------------------
identity              fdetienn@cisco.com
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
```

## DeviceDict subsets

### Subsets
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

### Filters
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

