#!/usr/bin/env python

from math import *
import matplotlib.pyplot as plt
import numpy as np

from datetime import *
import csv
import getpass
import sys

# http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def day_format(d):
    return lambda x, pos: date.fromtimestamp(86400 * (d + float(x))).strftime('%b %d')

def hour_format(h):
    return lambda x, pos: int(x) / h

prefix = getpass.getuser()

if (len(sys.argv) > 1):
    prefix = sys.argv[1]

log_file = ''.join([prefix, '/', 'kernel.log.out'])
log_iter = csv.reader(open(log_file, 'rb'), delimiter=' ')
log_len = file_len(log_file)

day = np.zeros(log_len)
hour = np.zeros(log_len)

for i, row in enumerate(log_iter):
    t = int(row[0])
    day[i] = floor(float(t) / 86400)
    hour[i] = float(t % 86400) / 3600

ndays = day.max() - day.min() + 1
hour_lev = 4

H, x, y = np.histogram2d(day, hour, bins=(ndays, hour_lev * 24))
H = np.minimum(H, 1)
H = H.transpose()
extent = [x[-1], x[0], y[0], y[-1]]

fig = plt.figure()

ax = plt.subplot(111)
ax.xaxis.set_major_formatter(plt.FuncFormatter(day_format(day.min())))
ax.yaxis.set_major_formatter(plt.FuncFormatter(hour_format(hour_lev)))
plt.yticks([0, 6*hour_lev, 12*hour_lev, 18*hour_lev])
img = plt.imshow(H, interpolation='nearest', cmap='gray')

plt.show()
