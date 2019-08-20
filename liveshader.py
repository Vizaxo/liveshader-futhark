#!/usr/bin/env python3

import sys
import numpy
from subprocess import call

filename = 'shader.fut' #sys.argv[1];
# TODO: set up opencl
call(['futhark', 'python', '--library', filename]);

import shader

shader = shader.shader()
n = shader.average(numpy.array([6.0, 4.0, 5.0]))
print(n)
