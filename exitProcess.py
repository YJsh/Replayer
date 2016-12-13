# -*- coding: gbk -*-
import subprocess


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
