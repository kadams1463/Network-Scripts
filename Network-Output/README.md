# Network Ouptut

- Author: Kevin Adams (kadams1463)
- Date:

## Prerequisites

- Python 3
  - All code is written for Python 3
- Netmiko
  - Needed for connecting to the devices.

## How to Use

- There are 3 files needed for this to work:
  - network-output.py - the script that grabs output
  - device.json - list of devices you want to capture output from
  - command_list.txt - list of all commands you want to run across the devices (preferrably the same type)

1. Edit the ```device.json``` file with your information
  - For the "device_type" item, please reference Netmiko's supported platforms: https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md
  - Example: ```cisco_ios```, ```cisco_asa```, ```juniper_junos```, etc.
1. Edit the ```command_list.txt``` file with your desired commands
1. Execute the Python script with the following:
```
python3 ./network-output.py
```

- NOTE: You might want to remove the example in the ```device.json``` file.
