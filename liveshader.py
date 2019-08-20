#!/usr/bin/env python3

import sys
import numpy
from subprocess import call
import time
import fcntl
import os
import signal
import pyinotify

filename = 'shader.fut' #sys.argv[1];
# TODO: set up opencl

def run_shader():
    call(['futhark', 'python', '--library', filename]);

    import shader

    shader = shader.shader()
    n = shader.average(numpy.array([6.0, 4.0, 5.0]))
    print(n)



def handler(signum, frame):
    print ("File %s modified" % (filename,))

class FileWatcher(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        run_shader()

def main():
    run_shader()
    wm = pyinotify.WatchManager()  # Watch Manager
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  | pyinotify.IN_MODIFY

    watcher = FileWatcher()
    notifier = pyinotify.Notifier(wm, watcher)
    wdd = wm.add_watch(filename, mask, rec=True)

    notifier.loop()

if(__name__ == "__main__"):
    main()
