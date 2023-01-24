#!/bin/usr/env python

# Author: Kevin Adams (kadams1463)
# Date: 7/21/2021

# Please see the README.md for more info.
# This script will download configs for network devices.
#
# It currently uses a username/password combination for this purpose. However, we can also tie this into AWS with Secrets Manager.


# MODULE IMPORT
# Import all the needed libraries for this script

from datetime import datetime # Will be used for datestamp
from netmiko import ConnectHandler # We're using netmiko to connect to network devices faster than paramiko
import sys
import os
import time # needed for times to handle the reaction times of network devices
import json # for reading JSON files

today = datetime.now() # get the current date and time

today_date = today.strftime("%m-%d-%Y_%H.%M")

file_name = ("output_")+(today_date) # create the  name of the file as a variable for the output

# FILE READING
# Read from the provided JSON files
device_list = './device.json' # List of devices we want to get output from

# ACTUAL DEVICES
# WITH loop to read through the device list
with open(device_list) as device_file: # open the device.json file to read from
    data = json.load(device_file)

# for each "device" object in the file, run through and get the type, hostname, the IP, username, password, and optional secret
    for device in data['device_list']:
        device1 = {
            'device_type': device['device_type'],
            'hostname': device['hostname'],
            'ip': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret']
        }

        try:
            # If one device doesn't work, continue with the rest of the loop
            net_connect = ConnectHandler(**device1)
            time.sleep(3)
            print(("Connected to host ")+(device['hostname'])+(" successfully!"))
        except:
            print(("Host ")+(device['hostname'])+(" is not reachable"))
            continue

        # Set the device_type for netmiko based on the value in the device.json file
        net_type = device['device_type']

        # open the command_list.txt file and read each line
        with open('command_list.txt') as c:
            command_list = c.readlines()

        # open a file to write to
        f = open(file_name, "a")

        # start the connection to the device
        with ConnectHandler(**device1) as net_connect:
            net_connect.enable() # switch to enable mode
            f.write("####################################\n") # format before hostname
            f.write(("### ")+(device['hostname'])+(" ###\n")) # write the device's hostname to the output to separate the output with formatting
            f.write("####################################\n\n") # format after hostname
            for command in command_list: # for loop to send the commands from the command_list.txt one at a time
                output = net_connect.send_command(command) # capture the output each time we send a command as a variable
                f.write((output)+("\n")) # write the output to the file
                time.sleep(2)
            net_connect.disconnect() # disconnect from the device
            time.sleep(2)

        f.close() # close the file
