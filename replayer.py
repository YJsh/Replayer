# -*- coding: gbk -*-
import socket
import time
import threading


class Replayer(threading.Thread):

    def __init__(self, events, device):
        super(Replayer, self).__init__()
        self.events = events
        self.device = device

    def run(self):
        self.device.setTCPPort()
        address = ("127.0.0.1", 1111)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.device.startMinitouch() as p:
            p.process.stdout.readline()
            s.connect(address)
            data = s.recv(512)
            print("data", data)
            for event in self.events:
                if event.startswith("sleep"):
                    time.sleep(float(event.split(" ")[1]))
                else:
                    if event.startswith("d") or event.startswith("m"):
                        pass
                    s.send(event + "\n")
            time.sleep(1)
            s.close()
