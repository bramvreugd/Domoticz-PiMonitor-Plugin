
# Update
Original maker was not happy and stopped to maintain this plugin.

I made a little change to this plugin to show a text a the throttled status in stead of only a number.



# PiMonitor
Python plugin to monitor temperature, memory usage, etc. from a Raspberry Pi.

If you want to monitor disk usage, look at https://github.com/Xorfor/Domoticz-Disc-usage-Plugin

## Prerequisites
Only works on Raspberry Pi

## Installation
1. Clone repository into your Domoticz plugins folder
    ```
    cd domoticz/plugins
    git clone https://github.com/Xorfor/Domoticz-PiMonitor-Plugin.git
    ```
1. Restart domoticz
    ```
    sudo service domoticz.sh restart
    ```
1. Make sure that "Accept new Hardware Devices" is enabled in Domoticz settings
1. Go to "Hardware" page
1. Enter the Name
1. Select Type: `PiMonitor`
1. Click `Add`

## Update
1. Go to plugin folder and pull new version
    ```
    cd domoticz/plugins/Domoticz-PiMonitor-Plugin
    git pull
    ```
1. Restart domoticz
    ```
    sudo service domoticz.sh restart
    ```

## Parameters
None

## Devices
The following devices are created:

| Name                | Description
| :---                | :---
| **Clock ARM**       | Clock ARM
| **Clock Core**      | Clock Core
| **Clock V3D**       | Clock V3D
| **Connections**     | Number of active network connections
| **Core voltage**    | Core voltage
| **CPU count**       | Number of CPUs/cores
| **CPU memory**      | Size of allocated memory for CPU
| **CPU temperature** | Shows the current CPU temperature
| **CPU speed**       | Current CPU speed
| **CPU usage**       | Percentage of CPU usage
| **Domoticz memory** | Amount of memory used by Domoticz
| **GPU memory**      | Size of allocated memory for GPU (specified with eg. raspi-config)
| **GPU temperature** | Shows the current GPU temperature
| **Host**            | Display hostname and ip address
| **Info**            | Display RPi info in the format: `Type: Processor - Memory (Manufacturer: Version)`
| **Latency**         | Latency to the gateway
| **Memory usage**    | Percentage of CPU memory in use
| **SDRAM C voltage** | SDRAM C voltage
| **SDRAM I voltage** | SDRAM I voltage
| **SDRAM P voltage** | SDRAM P voltage
| **Throttled**       | Throttled
| **Up time**         | Up time of the Pi, in sec, minutes, hours or days
