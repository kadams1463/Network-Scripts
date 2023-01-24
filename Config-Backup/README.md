# Config Backup

## Overview
The config-backup project is a script that uses JSON files for network administrators to retrieve and save configs via TFTP

## How it works
The script will read the contents of two JSON files: 1 for the TFTP IP address and 1 for the full device list.

Using those files, it will connect to each device one at a time and save to a TFTP server you run

Please note the following devices are currently supported:
* Brocade FastIron
* VyOS / EdgeOS

### AWS version of the script
* The script will use an AWS access key to read from Secrets Manager
  * Note this isn't really best practice, please see https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html

## How to use this script
1. Create 2 files in the same directory as the script
 1. device.json
 2. tftp.json

**NOTE:** Please feel free to use the files in the `<examples/>` directory as reference

2. Update both files with your information
 * "device_type" must match the same as the ones listed in [netmiko's documentation](https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md)

3. Run the script with:
```
python3 ./config-get.py
```

4. Files are saved with both hostname and datestamp.

### If using the AWS version of the script
1. Update your `~/.aws/credentials/` file with your access key
1. Edit the AWS region if needed (defaults to us-east-1)
1. Edit the following values in `aws-config-get.py` to your secret in Secrets Manager (i.e. prod/project-name/password-or-secret)
  * response1
  * response2
1. Run the script with:
```
python3 ./aws-config-get.py
```

## How to contribute
1. Branch the repository

2. Use .gitignore to ignore the JSON files in the current directory of the script
