# Scripting with radkit-client

`radkit-client` is a great interactive tool, but it is sometimes interesting to create reusable scripts.

There are 3 main categories of scripts:
1. scripts to import into `radkit-client` to augment its functionalities (e.g. new functions)
2. standalone scripts "execute-then-stop" subdivides into 2 categories
   1. easy-to-write, easy-to-deploy scripts that only depend on RADKit (ideal for scripting)
   2. professional code, with dependence on 3rd party libraries (ideal for proper application development)

This document focuses on use cases 1 and 2.i. The use-case 2.ii will be covered in a separate document.

## Augmenting radkit-client

Let's first focus on augmenting `radkit-client` interactive capabilities with pre-set functions.

### profile.py

A simple way to improve `radkit-client` is to add startup actions in the file `.radkit/client/profile.py` in your home directory (if the file does not exist, just create it).

`profile.py` is automatically read by `radkit-client` at startup and its content will be executed just as if you typed the commands at the prompt.

For instance add the following line to your `profile.py`:
```python
from radkit_client import ExecResultStatus, DeviceDict, Device
import regex as re
def show_ios_version(devices):
  if isinstance(devices, DeviceDict):
    ios = devices.filter("device_type", "IOS")
  elif isinstance(devices, Device):
    if devices.device_type == 'IOS':
      raise ValueError("Device not of type IOS")
    ios = devices.singleton()
  else:
    raise ValueError("'devices' must be of type Device or DeviceDict")

  show_ver = ios.exec("show version").wait()
  version_regex = re.compile("Version\s+(\S+)", flags=re.DOTALL)
  for name, device_result in show_ver.result.items():
    if device_result.status != ExecResultStatus.SUCCESS:
      print(f"no response from {name}")
      continue
    version = version_regex.findall(device_result.data)[0]
    print(f"{name} -> {version}")

show_ios_version(service.inventory)


client = sso_login("<your_cco_id>")
```

When you will start `radkit-client` the next time, you will immediately be authenticated and the `Client` obect will be in the variable `client`. Since this tends to be the very first command anyone types, this makes life more comfortable.

Once you connect to a service containing IOS devices, you can also use the function `show_ios_version(service.inventory)` to extract the IOS version from one or many devices.

For example:
```python
>>> show_ios_version(service.inventory)
c9800-1-fra-lab-net -> 16.11.01b
cifhqfs1-bn2-fra-lab-net -> 17.09.02a
ci9500-rack3-1-fra-lab-net -> 17.09.02
csr-cp-sda1-fra-lab-net -> 17.03.01a
l3rack6-2-fra-lab-net -> 03.11.02.E
ci9500-sd12-bn-fra-lab-net -> 17.09.02
l3rack2-1-fra-lab-net -> 16.09.02s
c3k-r3fs2-12-fra-lab-net -> 16.12.01s
l3-rack12-fralab-net -> 16.12.08
l3-rack14-fra-lab-net -> 03.07.01E
cifhqfs1-bn1-fra-lab-net -> 17.06.05
c3k-r3fs2-10-fra-lab-net -> 16.09.03s
l3-rack10-fra-lab-net -> 15.2(4)E10,
c3k-r3fs2-11-fra-lab-net -> 16.12.01s
csr-sdwan1-fra-lab-net -> 16.09.03
asr1k-lab-gw1-fra-lab-net -> 17.09.03a
l3-rack2-2-fra-lab-net -> 15.2(4)E1,
c3k-r3fs2-13-fra-lab-net -> 16.12.01s
ciasr1k-rack2-1-fra-lab-net -> 17.06.05
csr-sdwan2-fra-lab-net -> 16.09.03
l3-rack6-fra-lab-net -> 15.2(4)E10,
ci9500-sd11-bn-fra-lab-net -> 17.09.02
l3-rack13 -> 16.12.06
```

### Importing into radkit-client

It is of course possible to create and import any Python module into `radkit-client`. Simply define functions important to you in a file called (for instance) `my_radkit_functions.py` and simply import your module into `radkit-client` with the line:
```python
>>> import .my_radkit_functions
```

You can also import your own modules from `profile.py`.

## Standalone scripting with radkit-client

`radkit-client` interactive capabilities are nice, but it is sometimes useful to fully automate a task (execute a script, then return to the Command Shell).

In this case, simply write your script in a file, like any normal Python script, and tell `radkit-client` to execute it. There is one example file in this directory, called `simple_client_script.py`. To execute it, just use the following syntax from your Linux/Mac shell or Windows command prompt:
```
> radkit-client script simple_client_script.py
```
You can store this command into a shell script, potentially run it from your desktop, or start it in any way you see fit.

## Deactivate Loging

`radkit-client` displays details about RADKit while communicating with the RADKit Cloud or a RADKit Service. This information is useful to a user to be aware of possible error conditions.

In a script, these logs can be undesirable. They can be deactivated with the following 2 lines:

```python
from radkit_common import nglog
nglog.root.setLevel(nglog.CRITICAL)
```

`nglog` stands for "Next Generation Logging". `nglog` derives from Python logging but offers a lot of control in the logs coming from RADKit or the 3rd party libraries RADKit depends on. In particular, `nglog` is responsible for the audit trail generated by RADKit Service and RADKit Client.
