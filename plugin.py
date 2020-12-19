#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PiMonitor Plugin
#
# Author: Xorfor
"""
<plugin key="xfr-pimonitor" name="PiMonitor" author="Xorfor" version="4.1" wikilink="https://github.com/Xorfor/Domoticz-PiMonitor-Plugin">
    <params>
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
import socket
from enum import IntEnum, unique  # , auto


@unique
class unit(IntEnum):
    """
        Device Unit numbers

        Define here your units numbers. These can be used to update your devices.
        Be sure the these have a unique number!
    """

    CPUTEMP = 1
    GPUTEMP = 2
    RAMUSE = 3
    CPUUSE = 4
    CPUSPEED = 5
    UPTIME = 6
    CPUMEMORY = 7
    GPUMEMORY = 8
    CPUCOUNT = 9
    CONNECTIONS = 10
    COREVOLTAGE = 11
    SDRAMCVOLTAGE = 12
    SDRAMIVOLTAGE = 13
    SDRAMPVOLTAGE = 14
    DOMOTICZMEMORY = 15
    THROTTLED = 16
    INFO = 17
    HOST = 18
    LATENCY = 19
    CLOCK_ARM = 20
    CLOCK_V3D = 21
    CLOCK_CORE = 22


class BasePlugin:

    __HEARTBEATS2MIN = 6
    __MINUTES = 1

    __UNITS = [
        # Unit, Name, Type, Subtype, Options, Used
        [unit.CPUTEMP, "CPU temperature", 243, 31, {"Custom": "0;°C"}, 1],
        [unit.GPUTEMP, "GPU temperature", 243, 31, {"Custom": "0;°C"}, 1],
        [unit.RAMUSE, "Memory usage", 243, 31, {"Custom": "0;%"}, 1],
        [unit.CPUUSE, "CPU usage", 243, 31, {"Custom": "0;%"}, 1],
        [unit.CPUSPEED, "CPU speed", 243, 31, {"Custom": "0;Mhz"}, 1],
        [unit.UPTIME, "Up time", 243, 31, {"Custom": "0;sec"}, 1],
        [unit.CPUMEMORY, "CPU memory", 243, 31, {"Custom": "0;MB"}, 1],
        [unit.GPUMEMORY, "GPU memory", 243, 31, {"Custom": "0;MB"}, 1],
        [unit.CPUCOUNT, "CPU count", 243, 31, {}, 1],
        [unit.CONNECTIONS, "Connections", 243, 31, {}, 1],
        [unit.COREVOLTAGE, "Core voltage", 243, 31, {"Custom": "0;V"}, 1],
        [unit.SDRAMCVOLTAGE, "SDRAM C voltage", 243, 31, {"Custom": "0;V"}, 1],
        [unit.SDRAMIVOLTAGE, "SDRAM I voltage", 243, 31, {"Custom": "0;V"}, 1],
        [unit.SDRAMPVOLTAGE, "SDRAM P voltage", 243, 31, {"Custom": "0;V"}, 1],
        [unit.DOMOTICZMEMORY, "Domoticz memory", 243, 31, {"Custom": "0;KB"}, 1],
        [unit.THROTTLED, "Throttled", 243, 31, {}, 1],
        [unit.INFO, "Info", 243, 19, {}, 1],
        [unit.HOST, "Host", 243, 19, {}, 1],
        [unit.LATENCY, "Latency", 243, 31, {"Custom": "0;ms"}, 1],
        [unit.CLOCK_ARM, "Clock ARM", 243, 31, {"Custom": "0;Mhz"}, 1],
        [unit.CLOCK_V3D, "Clock V3D", 243, 31, {"Custom": "0;Mhz"}, 1],
        [unit.CLOCK_CORE, "Clock Core", 243, 31, {"Custom": "0;Mhz"}, 1],
    ]

    STYLE_OLD = 0
    STYLE_NEW = 1

    # Old
    OLD_STYLE = {
        # Code	Type	Revision	RAM	                Manufacturer    Processor
        0x0002: ["B", "1.0", "256 MB", "Egoman", "BCM2835"],
        0x0003: ["B", "1.0", "256 MB", "Egoman", "BCM2835"],
        0x0004: ["B", "2.0", "256 MB", "Sony UK", "BCM2835"],
        0x0005: ["B", "2.0", "256 MB", "Qisda", "BCM2835"],
        0x0006: ["B", "2.0", "256 MB", "Egoman", "BCM2835"],
        0x0007: ["A", "2.0", "256 MB", "Egoman", "BCM2835"],
        0x0008: ["A", "2.0", "256 MB", "Sony UK", "BCM2835"],
        0x0009: ["A", "2.0", "256 MB", "Qisda", "BCM2835"],
        0x000D: ["B", "2.0", "512 MB", "Egoman", "BCM2835"],
        0x000E: ["B", "2.0", "512 MB", "Sony UK", "BCM2835"],
        0x000F: ["B", "2.0", "512 MB", "Egoman", "BCM2835"],
        0x0010: ["B+", "1.2", "512 MB", "Sony UK", "BCM2835"],
        0x0011: ["CM1", "1.0", "512 MB", "Sony UK", "BCM2835"],
        0x0012: ["A+", "1.1", "256 MB", "Sony UK", "BCM2835"],
        0x0013: ["B+", "1.2", "512 MB", "Embest", "BCM2835"],
        0x0014: ["CM1", "1.0", "512 MB", "Embest", "BCM2835"],
        0x0015: ["A+", "1.1", "256 MB/512 MB", "Embest", "BCM2835"],
    }

    # New
    MEMORY_SIZE = {0: "256 MB", 1: "512 MB", 2: "1 GB", 3: "2 GB", 4: "4 GB", 5: "8 GB"}

    MANUFACTURER = {
        0: "Sony UK",
        1: "Egoman",
        2: "Embest",
        3: "Sony Japan",
        4: "Embest",
        5: "Stadium",
    }

    PROCESSOR = {0: "BCM2835", 1: "BCM2836", 2: "BCM2837", 3: "BCM2711"}

    TYPE = {
        0x00000000: "A",
        0x00000001: "B",
        0x00000002: "A+",
        0x00000003: "B+",
        0x00000004: "2B",
        0x00000005: "Alpha (early prototype)",
        0x00000006: "CM1",
        0x00000008: "3B",
        0x00000009: "Zero",
        0x0000000A: "CM3",
        0x0000000C: "Zero W",
        0x0000000D: "3B",
        0x0000000E: "3A+",
        0x0000000F: "Internal use only",
        0x00000010: "CM3+",
        0x00000011: "4B",
        0x00000013: "400",
        0x00000014: "CM4",
    }

    NUMBER_2_MEGA = 1 / 1000000

    def __init__(self):
        self.__runAgain = 0

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        else:
            Domoticz.Debugging(0)
        Domoticz.Debug("onStart called")
        # Validate parameters
        # --------------------------------------------------------------------------------
        # The provided images do, for some reason, conflit with Domoticz!!!
        # --------------------------------------------------------------------------------
        # Images
        # Check if images are in database
        # if "xfrpimonitor" not in Images:
        #     Domoticz.Image("xfrpimonitor.zip").Create()
        # image = Images["xfrpimonitor"].ID
        # Domoticz.Debug("Image created. ID: {}".format(image))
        #
        # Create devices
        for unit in self.__UNITS:
            if unit[0] not in Devices:
                Domoticz.Device(
                    Unit=unit[0],
                    Name=unit[1],
                    Type=unit[2],
                    Subtype=unit[3],
                    Options=unit[4],
                    Used=unit[5],
                    # Image=image,
                ).Create()
        # Log config
        DumpAllToLog()

    def onStop(self):
        Domoticz.Debug("onStop")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug(
            "onConnect {}={}:{} {}-{}".format(
                Connection.Name,
                Connection.Address,
                Connection.Port,
                Status,
                Description,
            )
        )

    def onMessage(self, Connection, Data):
        Domoticz.Debug(
            "onMessage {}={}:{}".format(
                Connection.Name, Connection.Address, Connection.Port
            )
        )

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand: {}, {}, {}, {}".format(unit, command, level, hue))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug(
            "onNotification: {}, {}, {}, {}, {}, {}, {}".format(
                name, subject, text, status, priority, sound, imagefile
            )
        )

    def onDisconnect(self, Connection):
        Domoticz.Debug(
            "onDisconnect {}={}:{}".format(
                Connection.Name, Connection.Address, Connection.Port
            )
        )

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat")
        self.__runAgain -= 1
        if self.__runAgain <= 0:
            self.__runAgain = self.__HEARTBEATS2MIN * self.__MINUTES
            #
            fnumber = getCPUcount()
            Domoticz.Debug("CPU count .........: {}".format(fnumber))
            UpdateDevice(unit.CPUCOUNT, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = getCPUtemperature()
            Domoticz.Debug("CPU temp ..........: {} °C".format(fnumber))
            UpdateDevice(unit.CPUTEMP, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = getGPUtemperature()
            Domoticz.Debug("GPU temp ..........: {} °C".format(fnumber))
            UpdateDevice(unit.GPUTEMP, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = getMemory("gpu")
            Domoticz.Debug("GPU memory ........: {} Mb".format(fnumber))
            UpdateDevice(unit.GPUMEMORY, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = getMemory("arm")
            Domoticz.Debug("CPU memory ........: {} Mb".format(fnumber))
            UpdateDevice(unit.CPUMEMORY, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = getCPUuse()
            Domoticz.Debug("CPU use ...........: {} %".format(fnumber))
            UpdateDevice(unit.CPUUSE, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = getRAMinfo()
            Domoticz.Debug("RAM use ...........: {} %".format(fnumber))
            UpdateDevice(unit.RAMUSE, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = getCPUcurrentSpeed()
            Domoticz.Debug("CPU speed .........: {} Mhz".format(fnumber))
            UpdateDevice(unit.CPUSPEED, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = round(getVoltage("core"), 2)
            Domoticz.Debug("Core voltage ......: {} V".format(fnumber))
            UpdateDevice(unit.COREVOLTAGE, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = round(getVoltage("sdram_c"), 2)
            Domoticz.Debug("SDRAM C ...........: {} V".format(fnumber))
            UpdateDevice(unit.SDRAMCVOLTAGE, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = round(getVoltage("sdram_i"), 2)
            Domoticz.Debug("SDRAM I ...........: {} V".format(fnumber))
            UpdateDevice(unit.SDRAMIVOLTAGE, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = round(getVoltage("sdram_p"), 2)
            Domoticz.Debug("SDRAM P ...........: {} V".format(fnumber))
            UpdateDevice(unit.SDRAMPVOLTAGE, int(fnumber), str(fnumber), TimedOut=0)
            #
            res = getCPUuptime()  # in sec
            Domoticz.Debug("Up time ...........: {} sec".format(res))
            fnumber = round(res, 2)
            options = {"Custom": "0;s"}
            if res >= 60:
                fnumber = round(res / (60), 2)
                options = {"Custom": "0;min"}
            if res >= 60 * 60:
                fnumber = round(res / (60 * 60), 2)
                options = {"Custom": "0;h"}
            if res >= 60 * 60 * 24:
                fnumber = round(res / (60 * 60 * 24), 2)
                options = {"Custom": "0;d"}
            UpdateDeviceOptions(unit.UPTIME, options)
            UpdateDevice(unit.UPTIME, int(fnumber), str(fnumber), TimedOut=0)
            #
            inumber = getNetworkConnections("ESTABLISHED")
            # inumber = getNetworkConnections("CLOSE_WAIT")
            Domoticz.Debug("Connections .......: {}".format(inumber))
            UpdateDevice(unit.CONNECTIONS, inumber, str(inumber), TimedOut=0)
            #
            fnumber = getDomoticzMemory()
            Domoticz.Debug("Domoticz memory ...: {} KB".format(fnumber))
            UpdateDevice(unit.DOMOTICZMEMORY, int(fnumber), str(fnumber), TimedOut=0)
            #
            inumber = getThrottled()
            Domoticz.Debug("Throttled .........: {}".format(inumber))
            UpdateDevice(unit.THROTTLED, inumber, str(inumber), TimedOut=0)
            #
            res = getPiRevision()
            # https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md
            # NOQuuuWuFMMMCCCCPPPPTTTTTTTTRRRR
            # ││││  ││││  │   │   │       ││││
            # ││││  ││││  │   │   │       └└└└─── R: Revision
            # ││││  ││││  │   │   └────────────── T: Type
            # ││││  ││││  │   └────────────────── P: Processor
            # ││││  ││││  └────────────────────── C: Manufacturer
            # ││││  │││└───────────────────────── M: Memory size
            # ││││  ││└────────────────────────── F: New flag
            # ││││  │└─────────────────────────── u: unused
            # ││││  └──────────────────────────── W: Warranty bit
            # │││└─────────────────────────────── u: unused
            # ││└──────────────────────────────── Q: OTP Read
            # │└───────────────────────────────── O: OTP Program
            # └────────────────────────────────── N: Overvoltage
            style = getBits(res, 23, 1)
            if style == self.STYLE_OLD:
                memory = self.OLD_STYLE.get(res)[2]
                manufacturer = self.OLD_STYLE.get(res)[3]
                soc = self.OLD_STYLE.get(res)[4]
                type = self.OLD_STYLE.get(res)[0]
                revision = self.OLD_STYLE.get(res)[1]
            else:  # style == STYLE_NEW:
                memory = self.MEMORY_SIZE.get(getBits(res, 20, 3))
                manufacturer = self.MANUFACTURER.get(getBits(res, 16, 4))
                soc = self.PROCESSOR.get(getBits(res, 12, 4))
                type = self.TYPE.get(getBits(res, 4, 8))
                revision = "{:.1f}".format(getBits(res, 0, 4))
            Domoticz.Debug(
                "Raspberry .........: {}: {} - {} ({}: {})".format(
                    type, soc, memory, manufacturer, revision
                )
            )
            #
            info = "{}: {} - {} ({}: {})".format(
                type, soc, memory, manufacturer, revision
            )
            UpdateDevice(unit.INFO, 0, info, TimedOut=0)
            #
            info = "{}: {}".format(getHostname(), getIP())
            UpdateDevice(unit.HOST, 0, info, TimedOut=0)
            #
            fnumber = getGatewayLatency()
            Domoticz.Debug("Latency ...........: {} ms".format(fnumber))
            UpdateDevice(unit.LATENCY, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = round(getClock("arm") * self.NUMBER_2_MEGA)
            Domoticz.Debug("Clock (arm) .......: {} Mhz".format(fnumber))
            UpdateDevice(unit.CLOCK_ARM, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = round(getClock("v3d") * self.NUMBER_2_MEGA)
            Domoticz.Debug("Clock (v3d) .......: {} Mhz".format(fnumber))
            UpdateDevice(unit.CLOCK_V3D, int(fnumber), str(fnumber), TimedOut=0)
            #
            fnumber = round(getClock("core") * self.NUMBER_2_MEGA)
            Domoticz.Debug("Clock (core) .......: {} Mhz".format(fnumber))
            UpdateDevice(unit.CLOCK_CORE, int(fnumber), str(fnumber), TimedOut=0)
            #
        else:
            Domoticz.Debug(
                "onHeartbeat called, run again in {} heartbeats.".format(
                    self.__runAgain
                )
            )


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


def DumpDevicesToLog():
    # Show devices
    Domoticz.Debug("Device count.........: {}".format(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device...............: {} - {}".format(x, Devices[x]))
        Domoticz.Debug("Device Idx...........: {}".format(Devices[x].ID))
        Domoticz.Debug(
            "Device Type..........: {} / {}".format(Devices[x].Type, Devices[x].SubType)
        )
        Domoticz.Debug("Device Name..........: '{}'".format(Devices[x].Name))
        Domoticz.Debug("Device nValue........: {}".format(Devices[x].nValue))
        Domoticz.Debug("Device sValue........: '{}'".format(Devices[x].sValue))
        Domoticz.Debug("Device Options.......: '{}'".format(Devices[x].Options))
        Domoticz.Debug("Device Used..........: {}".format(Devices[x].Used))
        Domoticz.Debug("Device ID............: '{}'".format(Devices[x].DeviceID))
        Domoticz.Debug("Device LastLevel.....: {}".format(Devices[x].LastLevel))
        Domoticz.Debug("Device Image.........: {}".format(Devices[x].Image))


def DumpImagesToLog():
    # Show images
    Domoticz.Debug("Image count..........: {}".format((len(Images))))
    for x in Images:
        Domoticz.Debug("Image '{}'...: '{}'".format(x, Images[x]))


def DumpParametersToLog():
    # Show parameters
    Domoticz.Debug("Parameters count.....: {}".format(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("Parameter '{}'...: '{}'".format(x, Parameters[x]))


def DumpSettingsToLog():
    # Show settings
    Domoticz.Debug("Settings count.......: {}".format(len(Settings)))
    for x in Settings:
        Domoticz.Debug("Setting '{}'...: '{}'".format(x, Settings[x]))


def DumpAllToLog():
    DumpDevicesToLog()
    DumpImagesToLog()
    DumpParametersToLog()
    DumpSettingsToLog()


def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=False):
    if Unit in Devices:
        if (
            Devices[Unit].nValue != nValue
            or Devices[Unit].sValue != sValue
            or Devices[Unit].TimedOut != TimedOut
            or AlwaysUpdate
        ):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            # Domoticz.Debug("Update {}: {} - '{}'".format(Devices[Unit].Name, nValue, sValue))


def UpdateDeviceOptions(Unit, Options={}):
    if Unit in Devices:
        if Devices[Unit].Options != Options:
            Devices[Unit].Update(
                nValue=Devices[Unit].nValue,
                sValue=Devices[Unit].sValue,
                Options=Options,
            )
            # Domoticz.Debug(
            #     "Device Options update: {} = {}".format(Devices[Unit].Name, Options)
            # )


# --------------------------------------------------------------------------------


options = {
    "measure_temp": ["temp", "'C"],
    "get_mem gpu": ["gpu", "M"],
    "get_mem arm": ["arm", "M"],
    "measure_clock core": ["frequency(1)", ""],
    "measure_clock arm": ["frequency(48)", ""],
    "measure_clock v3d": ["frequency(46)", ""],
    "measure_volts core": ["volt", "V"],
    "measure_volts sdram_c": ["volt", "V"],
    "measure_volts sdram_i": ["volt", "V"],
    "measure_volts sdram_p": ["volt", "V"],
    "get_throttled": ["throttled", "x0"],
}


def vcgencmd(option):
    """
        https://elinux.org/RPI_vcgencmd_usage
        https://github.com/nezticle/RaspberryPi-BuildRoot/wiki/VideoCore-Tools
    """
    if option in options:
        cmd = "/opt/vc/bin/vcgencmd {}".format(option)
        Domoticz.Debug("cmd: {}".format(cmd))
        try:
            res = os.popen(cmd).readline()
            Domoticz.Debug("res: {}".format(res))
            res = res.replace("{}=".format(options[option][0]), "")
            res = res.replace("{}\n".format(options[option][1]), "")
            Domoticz.Debug("res (replaced): {}".format(res))
        except:
            res = "0"
    else:
        res = "0"
    return float(res)


# --------------------------------------------------------------------------------

global _last_idle, _last_total
_last_idle = _last_total = 0


def getBits(value, start, length):
    return (value >> start) & 2 ** length - 1


def getClock(p):
    Domoticz.Debug("getClock p: {}".format(p))
    if p in [
        "arm",
        "core",
        "dpi",
        "emmc",
        "h264",
        "hdmi",
        "isp",
        "pixel",
        "pwm",
        "uart",
        "v3d",
        "vec",
    ]:
        res = vcgencmd("measure_clock {}".format(p))
        Domoticz.Debug("getClock measure_clock: {}".format(res))
    else:
        Domoticz.Debug("getClock: Invalid parameter")
        res = "0"
    return int(res)


def getCPUcount():
    return os.cpu_count()


def getCPUcurrentSpeed():
    # Return CPU speed in Mhz
    try:
        res = os.popen(
            "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
        ).readline()
    except:
        res = "0"
    return round(int(res) / 1000)


def getCPUtemperature():
    # Return CPU temperature
    try:
        res = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    except:
        res = "0"
    return round(float(res) / 1000, 1)


def getCPUuptime():
    try:
        with open("/proc/uptime") as f:
            fields = [float(column) for column in f.readline().strip().split()]
        res = round(fields[0])
    except:
        res = 0.0
    return res


def getCPUuse():
    """
        Return % of CPU used by user
        Based on: https://rosettacode.org/wiki/Linux_CPU_utilization#Python
    """
    global _last_idle, _last_total
    try:
        with open("/proc/stat") as f:
            fields = [float(column) for column in f.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - _last_idle, total - _last_total
        _last_idle, _last_total = idle, total
        res = round(100.0 * (1.0 - idle_delta / total_delta), 2)
    except:
        res = 0.0
    return res


def getDomoticzMemory():
    # ps aux | grep domoticz | awk '{sum=sum+$6}; END {print sum}'
    try:
        res = (
            os.popen("ps aux | grep domoticz | awk '{sum=sum+$6}; END {print sum}'")
            .readline()
            .replace("\n", "")
        )
    except:
        res = "0"
    return float(res)


def getGatewayLatency():
    try:
        gateway = (
            os.popen("route -n | awk '$1 == \"0.0.0.0\" { print $2 }'")
            .readline()
            .strip()
        )
        rtt = (
            os.popen("ping -c1 {} | grep rtt".format(gateway))
            .readline()
            .split()[3]
            .split("/")[0]
        )
    except:
        rtt = "0"
    return float(rtt)


def getGPUtemperature():
    # Return GPU temperature
    return float(vcgencmd("measure_temp"))


def getHostname():
    return socket.gethostname()


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 1))
    except socket.error:
        return None
    return s.getsockname()[0]


def getIP6():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    try:
        s.connect(("2001:4860:4860::8888", 1))
    except socket.error:
        return None
    return s.getsockname()[0]


def getMemory(p):
    if p in ["arm", "gpu"]:
        res = vcgencmd("get_mem {}".format(p))
    else:
        res = "0"
    return float(res)


def getNetworkConnections(state):
    # Return number of network connections
    res = 0
    try:
        for line in os.popen("netstat -tun").readlines():
            if line.find(state) >= 0:
                res += 1
    except:
        res = 0
    return res


def getPiRevision():
    try:
        res = (
            os.popen("cat /proc/cpuinfo | grep Revision\t")
            .readline()
            .replace("\n", "")
            .split(":")[1]
            .strip()
        )
        # Convert hex to int
        res = int(res, 16)
    except:
        res = None
    return res


def getRAMinfo():
    # Return RAM information in a list
    # Based on: https://gist.github.com/funvill/5252169
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
            return round(100 * int(res[1]) / int(res[0]), 2)


# http://www.microcasts.tv/episodes/2014/03/15/memory-usage-on-the-raspberry-pi/
# https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=164787
# https://stackoverflow.com/questions/22102999/get-total-physical-memory-in-python/28161352
# https://stackoverflow.com/questions/17718449/determine-free-ram-in-python
# https://www.reddit.com/r/raspberry_pi/comments/60h5qv/trying_to_make_a_system_info_monitor_with_an_lcd/


def getThrottled():
    return int(vcgencmd("throttled"))


def getUpStats():
    # Get uptime of RPi
    # Based on: http://cagewebdev.com/raspberry-pi-showing-some-system-info-with-a-python-script/
    # Returns a tuple (uptime, 5 min load average)
    try:
        s = os.popen("uptime").readline()
        load_split = s.split("load average: ")
        up = load_split[0]
        up_pos = up.rfind(",", 0, len(up) - 4)
        up = up[:up_pos].split("up ")[1]
        return up
    except:
        return ""


def getVoltage(p):
    # Get voltage
    # Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=30697
    if p in ["core", "sdram_c", "sdram_i", "sdram_p"]:
        res = vcgencmd("measure_volts {}".format(p))
    else:
        res = "0"
    return float(res)

