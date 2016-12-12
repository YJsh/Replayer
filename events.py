# -*- coding: utf-8 -*-
import subprocess
import time
import threading

import const


class ExitProcess(object):

    def __init__(self, args, **kwargs):
        super(ExitProcess, self).__init__()
        self._p = subprocess.Popen(args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._p.kill()

    @property
    def process(self):
        return self._p


deviceEvent = "/dev/input/event3"


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

    def __init__(self, process):
        super(Recorder, self).__init__()
        self.process = process
        self.minitouchEvents = []

    def run(self):
        try:
            self.recordEvents()
        except Exception, e:
            print(e)
        print("end")

    def recordEvents(self):
        posInfo = {0: SlotInfo()}
        slot = 0
        lastStamp = 0
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            if not line.startswith("[") or deviceEvent not in line:
                continue
            print(line.split())

            _, stamp, device, eventType, op, value = line.split()

            if value == "DOWN":
                value = 1
            elif value == "UP":
                value = 0
            else:
                value = int(value, 16)

            device = device[:-1]
            stamp = float(stamp[:-1])
            eventType = int(eventType, 16)
            op = int(op, 16)

            if not lastStamp:
                lastStamp = stamp

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
                posInfo[slot].x = value

            elif op == const.ABS_MT_POSITION_Y:
                posInfo[slot].y = value

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
                            "d %d %d %d %d\n" %
                            (idx, info.x, info.y, info.pressure))
                    else:
                        self.minitouchEvents.append(
                            "m %d %d %d %d\n" %
                            (idx, info.x, info.y, info.pressure))
                    info.isChanged = False
                self.minitouchEvents.append("c\n")


if __name__ == "__main__":
    with ExitProcess(["adb", "shell", "getevent", "-t"],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        t = Recorder(p.process)
        t.start()
        time.sleep(10)
        print(t.minitouchEvents)
