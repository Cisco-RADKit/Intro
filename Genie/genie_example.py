
# Script to be executed either from the radkit-client directly
# (copy paste inside radkit-client), OR called as such:
# radkit-client script genie_example.py

# Note : RADKit-Genie only works on linux/mac OS pip versions
# It's not part of the .exe/.pkg installers
#
# On windows, you install RADKit inside WSL
# to have support for radkit-genie

# User login and service connection

try:
   import radkit_genie
except:
    print("""
    RADKit Genie library not found. Genie is only available through PIP installers.
    On Windows, you must install WSL and install RADKit inside WSL to have support
    for RADKit genie, due to external libraries not native on Windows.

    Refer to https://radkit.cisco.com/docs/pages/compat.html for more info
    """)
    exit()

user_id = input("Enter your CCO user id:")
service_id = input("Enter your RADKit service id:")
client = sso_login(user_id)
service = client.service(service_id).wait()

# Filtering the inventory for IOS devices only
# ($ is regular expression character indicating end of the string,
# this is to filter out IOS-XR devices)

ios_devices = service.inventory.filter("device_type","IOS$")

# Executing a show ip interface brief and parsing it through Genie

intf_brief = ios_devices.exec("show ip interface brief").wait()
parsed_intf = radkit_genie.parse(intf_brief,os="iosxe")

# This should print the following:
#
#Showing Genie parsed output for cat8kv-1
# {
#     'interface': {
#         'GigabitEthernet1': {'ip_address': '198.18.1.101', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'},
#         'GigabitEthernet2': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'},
#         'GigabitEthernet3': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'},
#         'GigabitEthernet4': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'},
#         'C8000v#': {'ip_address': '', 'interface_is_ok': '', 'method': '', 'status': '', 'protocol': ''}
#     },
#     '_exclude': ['method', '(Tunnel.*)']
# }
# Showing Genie parsed output for iosv-1
# {
#     'interface': {
#         'GigabitEthernet0/0': {'ip_address': '198.18.1.11', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'},
#         'GigabitEthernet0/1': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'},
#         'GigabitEthernet0/2': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'},
#         'GigabitEthernet0/3': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'},
#         'Loopback0': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'unset', 'status': 'administratively down', 'protocol': 'down'},
#         'Iosv-1#': {'ip_address': '', 'interface_is_ok': '', 'method': '', 'status': '', 'protocol': ''}
#     },
#     '_exclude': ['method', '(Tunnel.*)']
# }


for device in parsed_intf:
    for command in parsed_intf[device].values():
        print(f"Showing Genie parsed output for {device}")
        print(command.data)
