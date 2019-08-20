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

sourcefile = sys.argv[1]
filename_base = os.path.splitext(sourcefile)[0]
working_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
filename_compiled = working_dir + 'shadercompiled'

def run_shader():
    print("Recompiling...")
    call(['futhark', 'pyopencl', '--library', sourcefile, '-o', filename_compiled])
    print("Recompiled")

    import shadercompiled
    importlib.reload(shadercompiled)

    shader = shadercompiled.shadercompiled()
    img = shader.main().get()
    print("Execution complete")

    plt.imshow(img, interpolation='nearest')
    plt.ion()
    plt.show()
    plt.pause(.001)

class FileWatcher(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        run_shader()

def main():
    run_shader()
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  | pyinotify.IN_MODIFY

    watcher = FileWatcher()
    notifier = pyinotify.Notifier(wm, watcher)
    wdd = wm.add_watch(sourcefile, mask, rec=True)

    notifier.loop()

if(__name__ == "__main__"):
    main()
