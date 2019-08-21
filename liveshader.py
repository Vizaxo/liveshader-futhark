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
import cv2
import tempfile

sourcefile = sys.argv[2]
filename_base = os.path.splitext(sourcefile)[0]
og_wd = os.getcwd() + '/'
sourcedir = os.path.dirname(og_wd + sourcefile) + '/'
working_dir = tempfile.mkdtemp() + '/'
os.chdir(working_dir)
filename_compiled = working_dir + 'shadercompiled'
sys.path.insert(1, working_dir)

def run_shader():
    print("Recompiling...")
    ret = call(['futhark', 'pyopencl', '--library', og_wd + sourcefile, '-o', filename_compiled])

    if (ret == 0):
        print("Executing...")
        import shadercompiled
        importlib.reload(shadercompiled)

        shader = shadercompiled.shadercompiled()
        img = shader.main().get()
        print("Execution complete")
        return img
    else:
        raise Exception("Compilation error")

def show_image(img):
    plt.imshow(img, interpolation='nearest')
    plt.ion()
    plt.show()
    plt.pause(.001)

def run_and_show():
    try:
        img = run_shader()
        show_image(img)
    except Exception as e:
        print (e)


class FileWatcher(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        run_and_show()

def write_image():
    image_name = sourcedir + filename_base + ".png"
    print("writing image " + image_name)
    try:
        img = run_shader()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(image_name, img)
    except Exception as e:
        print(e)

def watch():
    run_and_show()
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  | pyinotify.IN_MODIFY

    watcher = FileWatcher()
    notifier = pyinotify.Notifier(wm, watcher)
    wdd = wm.add_watch(sourcedir, mask, rec=True)

    notifier.loop()

def main():
    if (sys.argv[1] == "write"):
        write_image()
    elif (sys.argv[1] == "watch"):
        watch()
    else:
        print("invalid command " + sys.argv[1])

if(__name__ == "__main__"):
    main()
