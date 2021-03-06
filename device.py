# -*- coding: utf-8 -*-
import re
import subprocess
from exitProcess import ExitProcess


class Device(object):

    def __init__(self, deviceId="", deviceEvent="",
                 deviceResolution=None, deviceIp=("0.0.0.0", 0)):
        super(Device, self).__init__()
        self.deviceId = deviceId
        self.deviceEvent = deviceEvent
        self.deviceResolution = deviceResolution
        self.deviceIp = deviceIp
        self.deviceABI = None

    def connect(self):
        stdout = subprocess.check_output("adb connect %s:%d" % self.deviceIp)
        print(stdout)
        if stdout.startswith("unable to connect to"):
            raise RuntimeError("connect failed")
        self.deviceId = "%s:%d" % self.deviceIp
        return True

    def getDeviceId(self):
        """获取设备编号"""
        if not self.deviceId:
            stdout = subprocess.check_output("adb devices", shell=True)
            pattern = re.compile("([\w\d:.]+)\s+device\s*$")
            result = pattern.search(stdout)
            if not result:
                raise RuntimeError("Can not find avaliable device")
            self.deviceId = result.group(1)
        return self.deviceId

    def getDeviceEvent(self):
        """获取设备触屏事件"""
        if not self.deviceEvent:
            stdout = subprocess.check_output(
                    "adb -s %s shell getevent -p" % self.deviceId, shell=True)
            p = re.compile(r"0035.*max (\d+)")
            for line in stdout.split("\r\n"):
                if "/dev/input/event" in line:
                    event = line.split(" ")[-1][:-1]
                    continue
                if p.search(line):
                    break
            self.deviceEvent = event
        return self.deviceEvent

    def getDeviceResolution(self):
        """获取设备触屏分辨率"""
        if not self.deviceResolution:
            stdout = subprocess.check_output(
                "adb -s %s shell getevent -p %s" % (
                    self.deviceId, self.deviceEvent), shell=True)
            xPattern = re.compile(r"0035.*max (\d+)")
            yPattern = re.compile(r"0036.*max (\d+)")
            x = xPattern.search(stdout).group(1)
            y = yPattern.search(stdout).group(1)
            self.deviceResolution = (float(x), float(y))
        return self.deviceResolution

    def setTCPPort(self, port):
        """设置端口映射"""
        subprocess.call("adb -s %s forward tcp:%d localabstract:minitouch"
                        % (self.deviceId, port),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def startMinitouch(self):
        """启动minitouch"""
        return ExitProcess(
            ["adb", "-s", self.deviceId,
                    "shell", "/data/local/tmp/minitouch"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def pushMinitouch(self):
        """获取mititouch"""
        if not self.deviceABI:
            self.getABI()
        print(self.deviceABI)
        stdout = subprocess.check_output(
                "adb -s %s shell ls /data/local/tmp/minitouch"
                % self.deviceId, shell=True)
        if "No such file or directory" not in stdout:
            return
        subprocess.call("adb -s %s push libs/%s/minitouch /data/local/tmp/"
                        % (self.deviceId, self.deviceABI))
        subprocess.call("adb -s %s shell chmod 777 /data/local/tmp/minitouch"
                        % self.deviceId)

    def getABI(self):
        """获取系统ABI"""
        if not self.deviceABI:
            stdout = subprocess.check_output(
                    "adb -s %s shell getprop ro.product.cpu.abi"
                    % self.deviceId)
            self.deviceABI = stdout[0:stdout.find("\r")]
        return self.deviceABI


class DeviceMgr(object):

    def __init__(self):
        super(DeviceMgr, self).__init__()
        self.devices = []

    def getAllDevices(self):
        return self.devices

    def initDevices(self):
        stdout = subprocess.check_output("adb devices", shell=True)
        pattern = re.compile(r"([\w\d\:\.-]+)\s+device\s*$", re.M)
        result = pattern.findall(stdout)
        if not result:
            raise RuntimeError("Can not find avaliable device")
        for deviceId in result:
            self.devices.append(Device(deviceId=deviceId))

    def addDevice(self, ip, port):
        device = Device(deviceIp=(ip, port))
        self.devices.append(device)
        return device

    def findDeviceById(self, deviceId):
        for device in self.devices:
            if device.deviceId == deviceId:
                return device
        return None

    def findDeviceByIp(self, deviceIp):
        if type(deviceIp) == str:
            deviceIp = deviceIp.split(":")
            deviceIp = (deviceIp[0], int(deviceIp[1]))
        print(deviceIp)
        for device in self.devices:
            print(device.deviceIp)
            if device.deviceIp == deviceIp:
                return device
        return None


if __name__ == "__main__":
    mgr = DeviceMgr()
    mgr.initDevices()
    devices = mgr.getAllDevices()
    print(devices)
    d = devices[0]
    print(d.getDeviceId())
    print(d.getDeviceEvent())
    print(d.getDeviceResolution())
