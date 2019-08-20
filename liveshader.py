#!/usr/bin/env python3

import sys
import numpy
from subprocess import call
import time
import fcntl
import os
import signal
import pyinotify
import importlib
from matplotlib import pyplot as plt

filename = 'shader.fut' #sys.argv[1];
# TODO: set up opencl

def run_shader():
    print("Recompiling...")
    call(['futhark', 'python', '--library', filename]);

    import shader
    importlib.reload(shader)

    shader = shader.shader()
    img = shader.main(3)
    print("Execution complete")

    plt.imshow(img, interpolation='nearest')
    plt.ion()
    plt.show()
    plt.pause(.001)

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
