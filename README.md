# PiMonitor
Python plugin to monitor temperature, memory usage, etc. from a Raspberry Pi.

If you want to monitor disk usage, look at https://github.com/Xorfor/Domoticz-Disc-usage-Plugin

## Prerequisites
Only works on Raspberry Pi

## Parameters
None

## Devices
The following parameters are displayed:

| Name            | Description                                                        |
| :---            | :---                                                               |
| CPU temperature | Shows the current CPU temperature                                  |
| GPU temperature | Shows the current GPU temperature                                  |
| CPU memory      | Size of allocated memory for CPU                                   |
| GPU memory      | Size of allocated memory for GPU (specified with eg. raspi-config) |
| Memory usage    | Percentage of CPU memory in use                                    |
| CPU usage       | Percentage of CPU usage                                            |
| CPU speed       | Current CPU speed                                                  |
| CPU count       | Number of CPUs/cores                                               |
| Up time         | Up time of the Pi, in sec, minutes, hours or days                  |
| Connections     | Number of active network connections                               |

## To do
~~- [ ] Uptime. Due to a bug in Domoticz, not able to change the units in options~~
- [ ] Use psutil?

<!--
[![Github All Releases](https://img.shields.io/github/downloads/Xorfor/Domoticz-PiMonitor-Plugin/total.svg?style=plastic)](https://github.com/Xorfor/Domoticz-PiMonitor-Plugin/)

-->
