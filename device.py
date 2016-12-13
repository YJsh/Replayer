# -*- coding: gbk -*-
import re
import subprocess
from exitProcess import ExitProcess


class Device(object):

    def __init__(self, deviceId="", deviceEvent="", deviceResolution=None):
        super(Device, self).__init__()
        self.deviceId = deviceId
        self.deviceEvent = deviceEvent
        self.deviceResolution = deviceResolution

    def getDeviceId(self):
        """��ȡ�豸���"""
        if not self.deviceId:
            stdout = subprocess.check_output("adb devices", shell=True)
            pattern = re.compile("([\w\d:.]+)\s+device\s*$")
            result = pattern.search(stdout)
            if not result:
                raise RuntimeError("Can not find avaliable device")
            self.deviceId = result.group(1)
        return self.deviceId

    def getDeviceEvent(self):
        """��ȡ�豸�����¼�����Ҫ�û�ʹ�ô���"""
        if not self.deviceEvent:
            with ExitProcess(
                    ["adb", "shell", "getevent"], stdout=subprocess.PIPE) as p:
                events = {}
                num = 0
                while True:
                    num += 1
                    line = p.process.stdout.readline()
                    if not line.startswith("/dev/input/event"):
                        continue
                    index = line.split(" ")[0][-2]
                    events[index] = events.get(index, 0) + 1
                    if (events[index] << 2) > num:
                        self.deviceEvent = "/dev/input/event" + index
                        break
        return self.deviceEvent

    def getDeviceResolution(self):
        """��ȡ�豸�����ֱ���"""
        if not self.deviceResolution:
            stdout = subprocess.check_output(
                    "adb -s %s shell getevent -p %s" % (
                        self.deviceId, self.deviceEvent), shell=True)
            xPattern = re.compile(r"0035.*max (\d+)")
            yPattern = re.compile(r"0036.*max (\d+)")
            x = xPattern.search(stdout).group(1)
            y = yPattern.search(stdout).group(1)
            self.deviceResolution = (x, y)
        return self.deviceResolution

    def setTCPPort(self):
        """���ö˿�ӳ��"""
        subprocess.call("adb -s %s forward tcp:1111 localabstract:minitouch"
                        % self.deviceId,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def startMinitouch(self):
        """����minitouch"""
        return ExitProcess(
                ["adb", "-s", self.deviceId,
                    "shell", "/data/local/tmp/minitouch"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def pushMinitouch(self):
        """��ȡmititouch"""
        pass

    def getABI(self):
        """��ȡϵͳABI"""
        pass


if __name__ == "__main__":
    d = Device()
    print(d.getDeviceId())
    print(d.getDeviceEvent())
    print(d.getDeviceResolution())