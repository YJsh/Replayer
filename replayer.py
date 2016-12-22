# -*- coding: gbk -*-
import re
import socket
import time
import threading


class Replayer(threading.Thread):
    port = 1111

    def __init__(self, events, device):
        super(Replayer, self).__init__()
        self.events = events
        self.device = device

    def run(self):
        self.device.pushMinitouch()
        self.device.setTCPPort(Replayer.port)
        address = ("127.0.0.1", Replayer.port)
        Replayer.port += 1
        pattern = re.compile(r" [0-9]+ ([0-9]+) ([0-9]+) [0-9]+\n")
        with self.device.startMinitouch() as p:
            p.process.stdout.readline()
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(address)
                time.sleep(0.1)
                data = s.recv(1024)
                result = pattern.search(data)
                if result:
                    break
                s.close()
            x, y = result.groups()
            x, y = int(x), int(y)
            for event in self.events:
                if event.startswith("sleep"):
                    time.sleep(float(event.split(" ")[1]))
                else:
                    if event.startswith("d") or event.startswith("m"):
                        event = event.split(" ")
                        event[2] = str(int(float(event[2]) * x))
                        event[3] = str(int(float(event[3]) * y))
                        event = " ".join(event)
                        print(event)
                    s.send(event + "\n")
            time.sleep(1)
            s.close()
