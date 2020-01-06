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
1. Go to "Hardware" page and add new hardware with Type "PWS"
1. Enter the Port number as used in WS View
1. Press Add

## Update
1. Go to plugin folder and pull new version
    ```
    cd domoticz/plugins/Domoticz-PWS-Plugin
    git pull
    ```
1. Restart domoticz
    ```
    sudo service domoticz.sh restart
    ```

## Parameters
None

## Devices
The following parameters are displayed:

| Name                | Description
| :---                | :---
| **CPU temperature** | Shows the current CPU temperature
| **GPU temperature** | Shows the current GPU temperature
| **CPU memory**      | Size of allocated memory for CPU
| **GPU memory**      | Size of allocated memory for GPU (specified with eg. raspi-config)
| **Memory usage**    | Percentage of CPU memory in use
| **CPU usage**       | Percentage of CPU usage
| **CPU speed**       | Current CPU speed
| **CPU count**       | Number of CPUs/cores
| **Up time**         | Up time of the Pi, in sec, minutes, hours or days
| **Connections**     | Number of active network connections
| **Core voltage**    | Core voltage
| **SDRAM C voltage** | SDRAM C voltage
| **SDRAM I voltage** | SDRAM I voltage
| **SDRAM P voltage** | SDRAM P voltage
| **Domoticz memory** | Amount of memory used by Domoticz
| **Throttled**       | Throttled
| **Info**            | Display RPi info in the format: `Type: Processor - Memory (Manufacturer: Version)`
| **Host**            | Display hostname and ip address