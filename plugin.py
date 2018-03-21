#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PiMonitor Plugin
#
# Author: Xorfor
"""
<plugin key="xfr-pimonitor" name="PiMonitor" author="Xorfor" version="1.1.0" wikilink="https://github.com/Xorfor/Domoticz-PiMonitor-Plugin">
    <params>
        <!--
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="30px" required="true" default="80"/>
        -->
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import os

class BasePlugin:

    __HEARTBEATS2MIN = 6
    __MINUTES = 1

    # Device units
    _UNITS = {
        "CPUTEMP":      1,
        "GPUTEMP":      2,
        "RAMUSE":       3,
        "CPUUSE":       4,
        "CPUSPEED":     5,
        "UPTIME":       6,
        "CPUMEMORY":    7,
        "GPUMEMORY":    8,
        "CPUCOUNT":     9,
        "CONNECTIONS":  10,
        }

    def __init__(self):
        self.__runAgain = 0
        return

    def onStart(self):
        Domoticz.Debug("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)
        # Validate parameters
        # Images
        # Check if images are in database
        if "xfr_pimonitor" not in Images:
            Domoticz.Image("xfr_pimonitor.zip").Create()
        image = Images["xfr_pimonitor"].ID
        Domoticz.Debug("Image created. ID: "+str(image))
        # Create devices
        if len(Devices) == 0:
            Domoticz.Device(Unit=self._UNITS["CPUTEMP"], Name="CPU temperature", TypeName="Custom", Options={"Custom": "1;°C"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["GPUTEMP"], Name="GPU temperature", TypeName="Custom", Options={"Custom": "1;°C"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["GPUMEMORY"], Name="GPU memory", TypeName="Custom", Options={"Custom": "1;MB"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["CPUMEMORY"], Name="CPU memory", TypeName="Custom", Options={"Custom": "1;MB"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["CPUUSE"], Name="CPU usage", TypeName="Custom", Options={"Custom": "1;%"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["RAMUSE"], Name="Memory usage", TypeName="Custom", Options={"Custom": "1;%"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["CPUSPEED"], Name="CPU speed", TypeName="Custom", Options={"Custom": "1;Mhz"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["UPTIME"], Name="Up time", TypeName="Custom", Options={"Custom": "1;sec"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["CONNECTIONS"], Name="Connections", TypeName="Custom", Options={"Custom": "1;"}, Image=image, Used=1).Create()
            Domoticz.Device(Unit=self._UNITS["CPUCOUNT"], Name="CPU count", TypeName="Custom", Image=image, Used=1).Create()
        # Log config
        DumpConfigToLog()
        # Connection

    def onStop(self):
        Domoticz.Debug("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug(
            "onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(
            Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        self.__runAgain -= 1
        if self.__runAgain <= 0:
            self.__runAgain = self.__HEARTBEATS2MIN * self.__MINUTES
            # Execute your command
            #
            fnumber = getCPUcount()
            Domoticz.Debug("CPU count...: "+str(fnumber)+"")
            UpdateDevice(self._UNITS["CPUCOUNT"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getCPUtemperature()
            Domoticz.Debug("CPU temp....: "+str(fnumber)+" &deg;C")
            UpdateDevice(self._UNITS["CPUTEMP"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getGPUtemperature()
            Domoticz.Debug("GPU temp....: "+str(fnumber)+" &deg;C")
            UpdateDevice(self._UNITS["GPUTEMP"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getGPUmemory()
            Domoticz.Debug("GPU memory..: "+str(fnumber)+" Mb")
            UpdateDevice(self._UNITS["GPUMEMORY"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getCPUmemory()
            Domoticz.Debug("CPU memory..: "+str(fnumber)+" Mb")
            UpdateDevice(self._UNITS["CPUMEMORY"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getCPUuse()
            Domoticz.Debug("CPU use.....: "+str(fnumber)+" &#37;")
            UpdateDevice(self._UNITS["CPUUSE"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getRAMinfo()
            Domoticz.Debug("RAM use.....: "+str(fnumber)+" &#37;")
            UpdateDevice(self._UNITS["RAMUSE"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            fnumber = getCPUcurrentSpeed()
            Domoticz.Debug("CPU speed...: "+str(fnumber)+" Mhz")
            UpdateDevice(self._UNITS["CPUSPEED"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            res = getCPUuptime()  # in sec
            Domoticz.Debug("Up time.....: "+str(res)+" sec")
            # if res < 60:
            fnumber = round( res, 2 )
            UpdateDeviceOptions(self._UNITS["UPTIME"], {"Custom": "0;s"})
            if res >= 60:
                fnumber = round(res / (60), 2)
                UpdateDeviceOptions(self._UNITS["UPTIME"], {"Custom": "0;min"})
            if res >= 60 * 60:
                fnumber = round(res / (60 * 60), 2)
                UpdateDeviceOptions(self._UNITS["UPTIME"], {"Custom": "0;h"})
            if res >= 60 * 60 * 24:
                fnumber = round( res / ( 60 * 60 * 24 ), 2 )
                UpdateDeviceOptions(self._UNITS["UPTIME"], {"Custom": "0;d"})
            UpdateDevice(self._UNITS["UPTIME"], int(fnumber), str(fnumber), AlwaysUpdate=True)
            #
            inumber = getNetworkConnections("ESTABLISHED")
            #inumber = getNetworkConnections("CLOSE_WAIT")
            Domoticz.Debug("Connections.....: "+str(res))
            UpdateDevice(self._UNITS["CONNECTIONS"], inumber, str(inumber), AlwaysUpdate=True)
        else:
            Domoticz.Debug("onHeartbeat called, run again in " + str(self.__runAgain) + " heartbeats.")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

################################################################################
# Generic helper functions
################################################################################
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
        Domoticz.Debug("Device Options:   " + str(Devices[x].Options))
    for x in Settings:
        Domoticz.Debug("Setting:          " + str(x) + " - " + str(Settings[x]))

def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=False):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if Unit in Devices:
        if Devices[Unit].nValue != nValue \
                or Devices[Unit].sValue != sValue \
                or Devices[Unit].TimedOut != TimedOut \
                or AlwaysUpdate:
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Debug("Update " + Devices[Unit].Name + ": " + str(nValue) + " - '" + str(sValue) + "'")

def UpdateDeviceOptions(Unit, Options={}):
    if Unit in Devices:
        Devices[Unit].Update(nValue=Devices[Unit].nValue, sValue=Devices[Unit].sValue, Options=Options)
        Domoticz.Debug("Update options " + Devices[Unit].Name + ": " + str(Options))

# --------------------------------------------------------------------------------

global _last_idle, _last_total
_last_idle = _last_total = 0

# Return % of CPU used by user
# Based on: https://rosettacode.org/wiki/Linux_CPU_utilization#Python
def getCPUuse():
    global _last_idle, _last_total
    try:
        with open('/proc/stat') as f:
            fields = [float(column) for column in f.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - _last_idle, total - _last_total
        _last_idle, _last_total = idle, total
        res = round(100.0 * (1.0 - idle_delta / total_delta), 2 )
    except:
        res = 0.0
    return res

def getCPUcount():
    return os.cpu_count()

def getCPUuptime():
    try:
        with open('/proc/uptime') as f:
            fields = [float(column) for column in f.readline().strip().split()]
        res = round(fields[0])
    except:
        res = 0.0
    return res


# Return number of network connections
def getNetworkConnections(state):
    res = 0
    try:
        for line in os.popen("netstat -tun").readlines():
            if line.find(state) >= 0:
                res += 1
    except:
        res = 0
    return res

# Return GPU temperature
def getGPUtemperature():
    try:
        res = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline().replace("temp=", "").replace("'C\n", "")
    except:
        res = "0"
    return float(res)

def getGPUmemory():
    try:
        res = os.popen("/opt/vc/bin/vcgencmd get_mem gpu").readline().replace("gpu=", "").replace("M\n", "")
    except:
        res = "0"
    return float(res)

def getCPUmemory():
    try:
        res = os.popen("/opt/vc/bin/vcgencmd get_mem arm").readline().replace("arm=", "").replace("M\n", "")
    except:
        res = "0"
    return float(res)

# Return GPU temperature
def getCPUtemperature():
    try:
        res = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    except:
        res = "0"
    return round(float(res)/1000,1)

# Return CPU speed in Mhz
def getCPUcurrentSpeed():
    try:
        res = os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").readline()
    except:
        res = "0"
    return round(int(res)/1000)

# Return RAM information in a list
# Based on: https://gist.github.com/funvill/5252169
def getRAMinfo():
    p = os.popen("free -b")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            res = line.split()[1:4]
            # Index 0: total RAM
            # Index 1: used RAM
            # Index 2: free RAM
            return round(100 * int(res[1]) / int(res[0]), 2 )
# http://www.microcasts.tv/episodes/2014/03/15/memory-usage-on-the-raspberry-pi/
# https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=164787
# https://stackoverflow.com/questions/22102999/get-total-physical-memory-in-python/28161352
# https://stackoverflow.com/questions/17718449/determine-free-ram-in-python
# https://www.reddit.com/r/raspberry_pi/comments/60h5qv/trying_to_make_a_system_info_monitor_with_an_lcd/

# Get uptime of RPi
# Based on: http://cagewebdev.com/raspberry-pi-showing-some-system-info-with-a-python-script/
def getUpStats():
    #Returns a tuple (uptime, 5 min load average)
    try:
        s = os.popen("uptime").readline()
        load_split = s.split("load average: ")
        load_five = float(load_split[1].split(",")[1])
        up = load_split[0]
        up_pos = up.rfind(",", 0, len(up)-4)
        up = up[:up_pos].split("up ")[1]
        return up
    except:
        return ""
