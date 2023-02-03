#!/bin/usr/env python

# Author: Kevin Adams (kadams@)
# Date: 7/21/2021

# This script will download configs for network devices.
#
# It currently uses a username/password combination for this purpose.


# MODULE IMPORT
# Import all the needed libraries for this script

from datetime import datetime # Will be used for datestamp
from netmiko import ConnectHandler # We're using netmiko to connect to network devices faster than paramiko
import sys
import os
# import time # needed for times to handle the reaction times of network devices
import json # for reading JSON files



# DATE SETUP 
# Get the current date
today = datetime.now()

# Convert the date to a string
today_date = today.strftime("%m-%d-%Y")



# FILE READING
# Read from the provided JSON files
device_list = './device.json' # devices we want to save config from
tftp_list = './tftp.json' # TFTP server address

# Open the tftp.json file first to read the address
with open(tftp_list) as tftp_file: # read the variable for tftp_list and open as variable tftp_file
    tftp_ip = json.load(tftp_file) # set a new variable tftp_ip to read the contents of the file via JSON
print(("TFTP Server is : ")+(tftp_ip['ip'])) # print the value from key 'ip' in the tftp.json file
tftp_addr = tftp_ip['ip'] # use the same value provided for our TFTP IP address in our config saving commands


# ACTUAL DEVICES
# WITH loop to read through the device list
with open(device_list) as device_file: # similar to the TFTP one
    data = json.load(device_file)

    for device in data['device_list']:
        device1 = {
            'device_type': device['device_type'],
            'host': device['ip'],
            'username': device['username'],
            'password': device['password'],
            'secret': device['secret'],
        }

        try:
            # If one device doesn't work, continue with the rest of the loop
            net_connect = ConnectHandler(**device1)
            print(("Connected to host ")+(device['hostname'])+(" successfully!"))
        except:
            print(("Host ")+(device['hostname'])+(" is not reachable"))
            continue

        # Set the device_type for netmiko based on the value in the device.json file
        net_type = device['device_type']
        
        # If the values match
        if net_type == "cisco_ios":
            net_connect.enable() # switch to enable mode for Cisco
        if net_type == "brocade_fastiron":
            net_connect.enable() # switch to enable mode for brocade
        if net_type == "vyos":
            net_connect.send_command("configure", expect_string=r"#") # we're expecting the prompt to end in a "#" when going into configure mode
        
        # We need to save the file in the below format. To update, you need to make sure you're only adding string variables/data into each () set
        if net_type == "cisco_ios": # if it's a Cisco device
            net_connect.send_command(("copy running-config tftp://")+(tftp_addr)+("/")+(device['hostname'])+("_")+(today_date)+("_config"), expect_string="Address or name") # send the save command with some expected output from the device
            net_connect.send_command("\n", expect_string="Destination filename") # press Enter while expecting more output from the device
            net_connect.send_command("\n") # press Enter one more time to start the process
            print("Config saved.") # print a successful message
        if net_type == "brocade_fastiron": # if it's a Brocade device
            net_connect.send_command(("copy running-config tftp")+(tftp_addr)+(" ")+(device['hostname'])+("_")+(today_date)+("_config")) # send the save command for Brocade devices
            print("Config saved.") # print a successful message
        if net_type == "vyos": # if it's a VyOS device
            net_connect.send_command(("save tftp://")+(tftp_addr)+("/config_")+(device['hostname'])+("_")+(today_date)+(".boot")) # send the saver command for VyOS devices
            print("Config saved.") # print a successful message

        print("Config saved.")

        # Leave the current session and continue in the LOOP
        net_connect.disconnect()
