# Script to be executed either from the radkit-client directly
# (copy paste inside radkit-client), OR called as such:
# radkit-client script snmp_example.py

# User login and service connection

user_id = input("Enter your CCO user id:")
service_id = input("Enter your RADKit service id:")
client = sso_login(user_id)
service = client.service(service_id).wait()

# List all devices in inventory supporting SNMP

for dev in service.inventory.values():
    if dev.attributes.internal["snmp_config"]:
        print(f"{dev.name} supports SNMP")

# Should display something like:
# cat8kv-1 supports SNMP
# iosv-1 supports SNMP

# Performing an SNMPwalk on sys OID "1.3.6.1.2.1.1"

print("Running SNMP WALK for Sys oid")

sys_oid = service.inventory['cat8kv-1'].snmp.walk("1.3.6.1.2.1.1").wait()

print(str(sys_oid.result))

# Displaying the content of the sys_oid.result variable will display
#
# >>> sys_oid.result
# [SUCCESS] <radkit_client.sync.snmp.SNMPTable object at 0x11a246620>
# i    oid                value
# ---  -----------------  --------------------------------------------------------------------------------------------------------
# 0    1.3.6.1.2.1.1.1.0  'Cisco IOS Software [Cupertino], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.9.1a
# 1    1.3.6.1.2.1.1.2.0  '1.3.6.1.4.1.9.1.3004'
# 2    1.3.6.1.2.1.1.3.0  1108752
# 3    1.3.6.1.2.1.1.4.0  ''
# 4    1.3.6.1.2.1.1.5.0  'c8000v.cisco.com'
# 5    1.3.6.1.2.1.1.6.0  ''
# 6    1.3.6.1.2.1.1.7.0  78
# 7    1.3.6.1.2.1.1.8.0  0
#

# Print the value of one OID:
# Should display the device hostname

print("SNMP hostname retreived: ", sys_oid.result[(1, 3, 6, 1, 2, 1, 1, 5, 0)].value)
