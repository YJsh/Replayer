# -*- coding: gbk -*-
import re
import subprocess
import threading
import const


class SlotInfo(object):

    def __init__(self, x=0, y=0, pressure=50, key=const.KEY_NONE):
        self._x = x
        self._y = y
        self._pressure = pressure
        self._key = key
        self.isChanged = False

    def doChange(self):
        if not self.isChanged:
            self.isChanged = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self.doChange()
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self.doChange()
        self._y = value

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, value):
        self.doChange()
        self._pressure = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self.doChange()
        self._key = value


class Recorder(threading.Thread):

    def __init__(self, device=None):
        super(Recorder, self).__init__()
        self.minitouchEvents = []
        self.status = True
        self.device = device

    def changeStatus(self):
        self.status = not self.status

    def setDevice(self, device):
        self.device = device

    def getMinitouchEvents(self):
        return self.minitouchEvents

    def stop(self):
        self.process.kill()

    def run(self):
        try:
            deviceId = self.device.getDeviceId()
            deviceEvent = self.device.getDeviceEvent()
            print(deviceId, deviceEvent)
            self.process = subprocess.Popen(
                    "adb -s %s shell getevent -t %s" % (deviceId, deviceEvent),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("run")
            self.recordEvents()
        except Exception, e:
            print(e)
        print("end")
        self.process.kill()

    def recordEvents(self):
        posInfo = {0: SlotInfo()}
        slot = 0
        lastStamp = 0
        deviceEvent = self.device.getDeviceEvent()
        deviceX, deviceY = self.device.getDeviceResolution()
        print(deviceEvent)
        print("status: ", self.status)
        pattern = re.compile(r"\[\s*([\d\.]+)\s*\]\s+(\w+)\s+(\w+)\s+(\w+)")
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            if not self.status:
                continue

            result = pattern.match(line)
            stamp, eventType, op, value = result.groups()

            stamp = float(stamp[:-1])
            if not lastStamp:
                lastStamp = stamp
            eventType = int(eventType, 16)
            op = int(op, 16)

            if value == "DOWN":
                value = 1
            elif value == "UP":
                value = 0
            else:
                value = int(value, 16)

            if op == const.ABS_MT_TRACKING_ID:
                if value == int("ffffffff", 16):
                    posInfo[slot].key = const.KEY_UP
                else:
                    posInfo[slot].key = const.KEY_DOWN
            elif op == const.ABS_MT_SLOT:
                slot = value
                if slot not in posInfo:
                    posInfo[slot] = SlotInfo()
            elif op == const.ABS_MT_PRESSURE:
                posInfo[slot].pressure = value
            elif op == const.ABS_MT_POSITION_X:
                posInfo[slot].x = value / deviceX
            elif op == const.ABS_MT_POSITION_Y:
                posInfo[slot].y = value / deviceY
            elif op == const.SYN_REPORT:
                delay = stamp - lastStamp
                lastStamp = stamp
                self.minitouchEvents.append("sleep %f\n" % delay)
                for idx, info in posInfo.iteritems():
                    if not info.isChanged:
                        continue
                    if info.key == const.KEY_UP:
                        info.key = const.KEY_NONE
                        self.minitouchEvents.append("u %d\n" % idx)
                    elif info.key == const.KEY_DOWN:
                        info.key = const.KEY_NONE
                        self.minitouchEvents.append(
                            "d %d %f %f %d\n" % (
                                idx, info.x, info.y, info.pressure))
                    else:
                        self.minitouchEvents.append(
                            "m %d %f %f %d\n" % (
                                idx, info.x, info.y, info.pressure))
                    info.isChanged = False
                self.minitouchEvents.append("c\n")
        def tmp():
            if op == const.ABS_MT_TRACKING_ID:
                if value == int("ffffffff", 16):
                    posInfo[slot].key = const.KEY_UP
                else:
                    posInfo[slot].key = const.KEY_DOWN
            elif op == const.ABS_MT_SLOT:
                slot = value
                if slot not in posInfo:
                    posInfo[slot] = SlotInfo()
            elif op == const.ABS_MT_PRESSURE:
                posInfo[slot].pressure = value
            elif op == const.ABS_MT_POSITION_X:
                posInfo[slot].x = value / deviceX
            elif op == const.ABS_MT_POSITION_Y:
                posInfo[slot].y = value / deviceY
            elif op == const.SYN_REPORT:
                delay = stamp - lastStamp
                lastStamp = stamp
                self.minitouchEvents.append("sleep %f\n" % delay)
                for idx, info in posInfo.iteritems():
                    if not info.isChanged:
                        continue
                    if info.key == const.KEY_UP:
                        info.key = const.KEY_NONE
                        self.minitouchEvents.append("u %d\n" % idx)
                    elif info.key == const.KEY_DOWN:
                        info.key = const.KEY_NONE
                        self.minitouchEvents.append(
                            "d %d %f %f %d\n" % (
                                idx, info.x, info.y, info.pressure))
                    else:
                        self.minitouchEvents.append(
                            "m %d %f %f %d\n" % (
                                idx, info.x, info.y, info.pressure))
                    info.isChanged = False
                self.minitouchEvents.append("c\n")
