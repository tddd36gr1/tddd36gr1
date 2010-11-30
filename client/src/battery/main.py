from heapq import heappush, heappop
from Queue import Queue
import re
import sys
from socket import *
import thread
from threading import *
import gtk
import os
import osso
from time import *
import subprocess
#import dbus



def checkBattery():
    try:
        bus = dbus.SystemBus()
        hal_obj = bus.get_object ('org.freedesktop.Hal',
                                  '/org/freedesktop/Hal/Manager')
        hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
        uids = hal.FindDeviceByCapability('battery')
        dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
        x = float(dev_obj.GetProperty('battery.reporting.current'))
        y = float(dev_obj.GetProperty('battery.reporting.design'))
        bat = int((x/y)*100)
        if(bat < 100):
            print 'Nu har du',bat,'% kvar i batteri.'
    except Exception, e :
        print "Du sitter pa en loser dator och har inget batteri"