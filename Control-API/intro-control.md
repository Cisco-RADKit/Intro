# Introduction to RADKit Control API

## Preamble
RADKit Service offers a Web UI to manage RADKit Service. From the WebUI, an administrator can control the inventory (add, remove, modify devices), remote user access (manage users, role-based access control, ...) and many more administrative tasks.

The Web UI is built on top of a REST API, which is wrapped into a Python API. For this reason, the whole set of APIs to control RADKit Service is aptly named the RADKit Control API (or simply the Control API for short).

The Control API is only available "locally", i.e. the process calling the Control API must have direct API connectivity to the RADKit Service. The Control API is also gated by administrator credentials: the API client must authenticate using adminstrator (including superadmin) credentials.

It is possible to expose the Control API to remote users, but this is out of the scope of this introduction.

:warning: In this document, we will use object names Service, Device, ... The names are the same as the RPC equivalent object as they represent the same underlying entity. It is important to realize however that the methods available on the Control API objects are completely different from the equivalen RPC API objects. The Control API objects are meant to manage the RADKit Service, while the RPC API objects are meant to query the physical devices.

## Connecting to a RADKit Service Control API

The first thing to do is to create a Python context offering an authenticated connection to RADKit Service.

For the purpose of this exercise, we need a RADKit Service - you can create one on your own computer; it will be accessible on `localhost:8081`. Since this vanilla RADKit Service is likely fitted with default self-signed certificates, certificate validation must be omitted.
We can achieve that by creating an ssl context using `create_public_ssl_context()`:
```python
verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)
```

The context can now be created:
```python
password = getpass("superadmin password: ")
with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=password, http_client_kwargs=dict(verify=verify)) as service:
```

The above context will authenticate as `superadmin` on the RADKit service running on your local computer (`localhost`).

:warning: it is **VERY BAD SECURITY PRACTICE** to store passwords in your scripts and automations. One mistake, and those passwords end up in a public GIT repository, or on an online backup, for any attacker to harvest.

## Create a device object
Now let's create a device representation in memory (object). From a Control API standpoint, a device is a JSON object. However, RADKit offers pydantic equivalent, allowing you to code more efficiently, and safely.

If you are unfamiliar with Pydantic, visit https://pydantic.dev.

In a nutshell, Pydantic offers Python object representations similar to a Pyhthon Data Classes or a C struct. In addition, at creation time, Pydantic will validate and make sure the data matches the expected format for each field.

```python
    device = NewDevice(
        name="new-device",
        host="10.0.0.1",
        deviceType="IOS",
        enabled=True,
    )
```
## Create the device on RADKit Service

To create the device on RADKit Service, use the `create_device()` member function from the `service` object:
```python
    result = service.create_device(device)
```


