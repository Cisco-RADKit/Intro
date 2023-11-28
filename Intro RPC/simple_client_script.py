# with a client script, enter your code exactly as you would do in radkit-client.
# only import the extra modules you need.
# run it with the following command:
# radkit-client script simple_client_script.py

import regex as re
# import ExecResultStatus from the radkit_client library to verify status
from radkit_client import ExecResultStatus

user_id = input("Enter your CCO user id: ")
service_id = input("Enter the service id: ")

client = sso_login(user_id)
service = service=client.service(service_id).wait()

# select IOS and Linux devices
ios = service.inventory.filter("device_type", "IOS")
linux = service.inventory.filter("device_type", "LINUX")

# Queue some commands
ios_versions = ios.exec("show version")
linux_versions = linux.exec("uname -a")

# Now wait for command completion on both Linux and IOS
ios_versions.wait()
linux_versions.wait()

ios_version_regex = re.compile("Version\s+(\S+),", flags=re.DOTALL)
for name, device_result in ios_versions.result.items():
  if device_result.status != ExecResultStatus.SUCCESS:
    print(f"no response from {name}")
    continue
  version = ios_version_regex.findall(device_result.data)[0]
  print(f"{name} -> {version}")

linux_version_regex = re.compile("Version\s+(\S+):", flags=re.DOTALL)
for name, device_result in linux_versions.result.items():
  if device_result.status != ExecResultStatus.SUCCESS:
    print(f"no response from {name}")
    continue
  version = linux_version_regex.findall(device_result.data)[0]
  print(f"{name} -> {version}")

