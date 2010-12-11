import dbus
import os
import time
import threading
import gtk
import gui

"""
Function that return an int value of the clients battery percent
"""

class Battery_check(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
    
    def getBatteryPercent(self):
        bus = dbus.SystemBus()
        hal_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
        hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
        uids = hal.FindDeviceByCapability('battery')
        dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
        return dev_obj.GetProperty('battery.charge_level.percentage')
    
    """
    Functions that set the brightness of the screen to a
    value between 0-251
    """
    def lowerBrightness(self):
        os.system('chroot /mnt/initfs dsmetest -l 50')
        ##pittar
        
    def higherBrightness(self):
        os.system('chroot /mnt/initfs dsmetest -l 250')
    
    def run(self):
        """
        If the batterypercent getting lower than 26, calling lowerBrightness
        Else call higherBrightness
        """
        while 1:
            x = self.getBatteryPercent()
            if (x < 26):
                self.lowerBrightness()
                gtk.gdk.threads_enter()
                gui.notify_battery()
                gtk.gdk.threads_leave()
            elif (x > 26):
                self.higherBrightness()

            time.sleep(60)
                
def start():
    global battery_check
    battery_check = Battery_check()
    battery_check.start()
    
def getBatteryPercent():
    return battery_check.getBatteryPercent()