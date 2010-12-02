import dbus

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
