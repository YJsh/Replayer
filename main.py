# -*- coding: utf-8 -*-
from exitProcess import ExitProcess
from ui.mainUI import run

if __name__ == "__main__":
    with ExitProcess("adb start-server") as p:
        p.process.communicate()
    run()
    with ExitProcess("adb kill-server") as p:
        p.process.communicate()
