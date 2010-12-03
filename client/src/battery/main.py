import dbus
import os

"""
Function that return an int value of the clients battery percent
"""
def getBatteryPercent():
    bus = dbus.SystemBus()
    hal_obj = bus.get_object ('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
    hal = dbus.Interface (hal_obj, 'org.freedesktop.Hal.Manager')
    uids = hal.FindDeviceByCapability('battery')
    dev_obj = bus.get_object ('org.freedesktop.Hal', uids[0])
    return dev_obj.GetProperty('battery.charge_level.percentage')

"""
Function that set the brightness of the screen to 50
(values between 0-251 could be set)
"""
def changeBrightness():
    os.system('chroot /mnt/initfs dsmetest -l 50')

"""
If the batterypercent getting lower than 26, calling changeBrightness
"""
while 1:
    if (getBatteryPercent() < 26):
        changeBrightness()
        break