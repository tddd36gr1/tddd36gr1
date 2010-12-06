'''
Advanced Power Monitor
2008-2009(c) Kirill Plyashkevich <ru.spirit@gmail.com>
Connects to bunch of dbus signals, monitors values change and emmits signal in case of update.
'''

import gobject
import os, subprocess
if not subprocess:
  import commands
import dbus, dbus.service
from dbus.mainloop.glib import DBusGMainLoop

class apm(dbus.service.Object):

  version = '0.4.1'
  iface = "ru.spirit.advanced_power_monitor"
  opath = "/ru/spirit/advanced_power_monitor"
  signals = {}
  interfaces = {}
  charging = False
  full = False
  charger_disconn = False
  working = True
  signal_queue = []
  min_queue = 1

  def __init__(self):
    self.m_loop = DBusGMainLoop()
    self.bus = dbus.SystemBus(mainloop = self.m_loop, private = True)
    self.bus_name = dbus.service.BusName(self.iface, self.bus) 
    dbus.service.Object.__init__(self, self.bus_name, self.opath)

    self.ifaces_map = {'BME': ('org.freedesktop.Hal', '/org/freedesktop/Hal/devices/bme', 'org.freedesktop.Hal.Device'),
                       'MCE': ('com.nokia.mce', '/com/nokia/mce/request', 'com.nokia.mce.request'),
                       'CPUFreq':('org.freedesktop.Hal', '/org/freedesktop/Hal/devices/computer', 'org.freedesktop.Hal.Device.CPUFreq')
                      }

    self.signals_map = {'hal_PropertyModified': {'path': '/org/freedesktop/Hal/devices/bme', 'dbus_interface': 'org.freedesktop.Hal.Device', 'signal_name': 'PropertyModified', 'cb': self._property_modified_handler},
                        'bme_battery_timeleft': {'path': '/com/nokia/bme/signal', 'dbus_interface': 'com.nokia.bme.signal', 'signal_name': 'battery_timeleft', 'cb': self._battery_timeleft},
                        'bme_charger_charging_on': {'path': '/com/nokia/bme/signal', 'dbus_interface': 'com.nokia.bme.signal', 'signal_name': 'charger_charging_on', 'cb': self._battery_charging_on_handler},
                        'bme_charger_charging_off': {'path': '/com/nokia/bme/signal', 'dbus_interface': 'com.nokia.bme.signal', 'signal_name': 'charger_charging_off', 'cb': self._battery_charging_off_handler},
                        'bme_charger_disconnected': {'path': '/com/nokia/bme/signal', 'dbus_interface': 'com.nokia.bme.signal', 'signal_name': 'charger_disconnected', 'cb': self._battery_charger_disconnected},
                        'bme_battery_full': {'path': '/com/nokia/bme/signal', 'dbus_interface': 'com.nokia.bme.signal', 'signal_name': 'battery_full', 'cb': self._battery_full_handler},
                        'mce_device_mode': {'path': '/com/nokia/mce/signal', 'dbus_interface': 'com.nokia.mce.signal', 'signal_name': 'sig_device_mode_ind', 'cb':  self._mce_device_mode_handler}
                       }

    self.init_signals()
    self.init_interfaces()

    self.has_light_sensor = os.path.exists("/usr/lib/mce/modules/libfilter-brightness-als.so") and os.path.exists("/usr/lib/mce/modules/libfilter-brightness-simple.so")
    self.info_map = {'battery-status': {'value': 0},
                     'battery-reporting-design': {'value': self.interfaces['BME'].GetPropertyInteger(u'battery.reporting.design')},
                     'timeleft-idle': {'value': -1},
                     'timeleft-active': {'value': -1},
                     'fn-device-mode': {'value': self.interfaces['MCE'].get_device_mode()},
                     'cpu-frequency': {'value': 0, 'time': 5000, 'cb': self.update_cpu_frequency},
                     'cpu-governor': {'value': self.interfaces['CPUFreq'].GetCPUFreqGovernor(), 'time': 5000, 'cb': self.update_cpu_governor},
                     'cpu-governors': {'value': self.interfaces['CPUFreq'].GetCPUFreqAvailableGovernors()},
                     'temperature': {'value': 0, 'time': 10000, 'cb': self.update_internal_temperature},
                     'light-sensor': {'value': 0, 'time': 10000, 'cb': self.update_light_sensor_data},
                     'uptime': {'value': 0, 'time': 60000,'cb': self.update_uptime},
                     'version': {'value': ''},
                     'free-ram': {'value': 0},
                     'total-ram': {'value': self.process_meminfo(self.get_file_content_lines("/proc/meminfo"), ['MemTotal'])},
                     'free-swap': {'value': 0},
                     'total-swap': {'value': 0},
                     'free-mem': {'value': 0, 'time': 5000, 'cb': self.update_mem},
                     'total-mem': {'value': 0},
                     'free-diskspace': {'value': [], 'time': 300000, 'cb': self.update_free_diskspace}
                }
    self.update_info()

#Signal receivers

#Object path: /org/freedesktop/Hal/devices/bme
#Interface: org.freedesktop.Hal.Device
#Signal: PropertyModified
  def _property_modified_handler(self, value, props):
    signals = [str(x[0]) for x in props]
    if 'battery.remaining_time' in signals:
      self.get_timeleft_info()
    if 'battery.reporting.current' in signals:
      self.update_percent()
#end

#Object path: /com/nokia/bme/signal
#Interface: com.nokia.bme.signal

#Signal: battery_timeleft
  def _battery_timeleft(self, idle_time, active_time):
    self.check_property_modified(['timeleft-idle', idle_time], ['timeleft-active', active_time])

#Signal: charger_charging_on
  def _battery_charging_on_handler(self):
    self.charging = True
    self.charger_disconn = False
    self.set_value('battery-status', -1)
    self.PropertyModified(['battery-status'])

#Signal: charger_charging_off
  def _battery_charging_off_handler(self):
    self.full = False
    self.charging = False

#Signal: charger_disconnected
  def _battery_charger_disconnected(self):
    self.full = False
    self.charging = False
    self.charger_disconn = True
    self.set_value('battery-status', -1)
    self.PropertyModified(['battery-status'])
    self.update_percent()

#Signal: battery_full
  def _battery_full_handler(self):
    self.full = True
    self.PropertyModified(['battery-status'])
#end

#Object path: /com/nokia/mce/signal
#Interface: com.nokia.mce.signal
#Signal: sig_device_mode_ind
  def _mce_device_mode_handler(self, signal):
    self.PropertyModified(['fn-device-mode'])
    signal = str(signal)
    if signal in ['normal', 'flight']:
      self.check_property_modified(['fn-device-mode', signal])
#end

#Signals subsystem
  def init_signals(self):
    for x  in self.signals_map:
      try:
        self.signals[x] = self.bus.add_signal_receiver(self.signals_map[x]['cb'], signal_name=self.signals_map[x]['signal_name'], dbus_interface=self.signals_map[x]['dbus_interface'], path=self.signals_map[x]['path'])
      except:
        pass

  def destroy_signals(self):
    for key in self.signals:
      self.bus._clean_up_signal_match(self.signals[key])
      self.bus.remove_signal_receiver(self.signals[key])
#end

#Interfaces subsystem
  def init_interfaces(self):
    for x in self.ifaces_map:
      try:
        self.interfaces[x] = dbus.Interface(self.bus.get_object(self.ifaces_map[x][0], self.ifaces_map[x][1]), self.ifaces_map[x][2])
      except:
        pass

  def destroy_interfaces(self):
    for key in self.interfaces:
      self.interfaces[key] = None
#end

  def _cleanup(self):
    for x in self.info_map:
      if 'src_evt' in self.info_map[x] and self.info_map[x]['src_evt']:
        gobject.source_remove(self.info_map[x]['src_evt'])
    self.destroy_signals()
    self.destroy_interfaces()

  def update_info(self):
    self.get_status_info()
    self.get_timeleft_info()
    self.update_percent()
    self.update_os_version('version')
    for x in self.info_map:
      if 'cb' in self.info_map[x]:
        self.info_map[x]['cb'](x)
    return self.working

  @dbus.service.signal(dbus_interface='ru.spirit.advanced_power_monitor.signal', signature='as')
  def PropertyModified(self, keys):
    return keys

  def notify(self, keys):
    c_queue = len(keys)/2
    if c_queue > self.min_queue:
      self.min_queue = c_queue
    self.signal_queue.extend(keys)
    result = set(self.signal_queue)
    if len(result) > self.min_queue:
      self.signal_queue = []
      self.PropertyModified(result)

#Section: Battery time left
#Key: timeleft-idle, timeleft-active
  def get_timeleft_info(self):
    self.run_shell_command('run-standalone.sh /usr/bin/dbus-send --system --type=signal /com/nokia/bme/request com.nokia.bme.request.timeleft_info_req')
#end

#Section: Battery state and percentage
#Key: battery-state
  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request')
  def get_status_info(self):
    self.run_shell_command('run-standalone.sh /usr/bin/dbus-send --system --type=signal /com/nokia/bme/request com.nokia.bme.request.status_info_req')

  def update_percent(self):
    self.check_property_modified(['battery-status', min(100.0, round(100.0 * self.interfaces['BME'].GetPropertyInteger(u'battery.reporting.current')/self.get_value('battery-reporting-design'), 1))])

  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request', out_signature='s')
  def get_battery_state(self):
    result = 'unknown'
    if self.full:
      result = 'full'
    elif self.charging:
      result = 'charging'
    elif self.charger_disconn:
      result = 'charger_disconn'
      self.charger_disconn = False
    else:
      result = str(self.get_value('battery-status')) + "%"
    return result
#end

#Section: MCE
#Key: device-mode
  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request')
  def home_key_pressed_long(self):
    self.run_shell_command('run-standalone.sh /usr/bin/dbus-send --system --type=signal /com/nokia/mce/signal com.nokia.mce.signal.sig_home_key_pressed_long_ind')

  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request')
  def home_key_pressed(self):
    self.run_shell_command('run-standalone.sh /usr/bin/dbus-send --system --type=signal /com/nokia/mce/signal com.nokia.mce.signal.sig_home_key_pressed_ind')

  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request')
  def switch_device_mode(self):
    if self.get_value('fn-device-mode') == "normal":
      self.set_value('fn-device-mode', "flight")
    elif self.get_value('fn-device-mode') == "flight":
      self.set_value('fn-device-mode', "normal")
    if 'MCE' in self.interfaces:
      self.interfaces['MCE'].req_device_mode_change(self.get_value('fn-device-mode'))

  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request')
  def tklock_device(self):
    if 'MCE' in self.interfaces:
      self.interfaces['MCE'].req_tklock_mode_change("locked")
 
  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request')
  def reboot(self):
    if 'MCE' in self.interfaces:
      self.interfaces['MCE'].req_reboot()
    else:
      self.run_shell_command('/sbin/reboot -n')

  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request')
  def shutdown(self):
    if 'MCE' in self.interfaces:
      self.interfaces['MCE'].req_shutdown()
    else:
      self.run_shell_command('/sbin/shutdown -n')
#end

#Section: CPU
#Key: cpu-governor, cpu-frequency
  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request', in_signature='s')
  def set_cpu_governor(self, governor):
    if not self.info_map['cpu-governor']['value'] == governor and governor in self.info_map['cpu-governors']['value']:
      if 'CPUFreq' in self.interfaces and governor in self.get_value('cpu-governors'):
        self.interfaces['CPUFreq'].SetCPUFreqGovernor(governor)
        self.check_property_modified(['cpu-governor', governor])

  def update_cpu_governor(self, key):
    if 'CPUFreq' in self.interfaces:
      self.check_property_modified([key, self.interfaces['CPUFreq'].GetCPUFreqGovernor()])
    self.add_timer_event(key)
    return False

  def update_cpu_frequency(self, key):
    lines = self.get_file_content_lines("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
    if lines:
      self.check_property_modified([key, long(lines[0])/1000])
    self.add_timer_event(key)
    return False
#end

#Section: OS Version
#Key: version
  def update_os_version(self, key):
    lines = self.get_file_content_lines("/etc/osso_software_version")
    if lines:
      self.check_property_modified([key, lines[0].rsplit('_')[2]])
    return False
#end

#Section: Internal temperature
#Key: temperature
  def update_internal_temperature(self, key):
    lines = self.get_file_content_lines("/sys/devices/platform/i2c_omap.1/i2c-1/1-0048/temp1_input")
    if lines:
      self.check_property_modified([key, long(lines[0])/1000.0])
    self.add_timer_event(key)
    return False
#end

#Section: Light sensor
#Key: light-sensor
  def update_light_sensor_data(self, key):
    if self.has_light_sensor:
      lines = self.get_file_content_lines("/sys/devices/platform/i2c_omap.2/i2c-0/0-0029/lux")
      if lines:
        self.check_property_modified([key, long(lines[0])])
      self.add_timer_event(key)
    return False
#end

#Section: Uptime
#Key: uptime
  def update_uptime(self, key):
    lines = self.get_file_content_lines("/proc/uptime")
    if lines:
      self.check_property_modified([key, long(lines[0].rsplit(".")[0])])
    self.add_timer_event(key)
    return False
#end

#Section: RAM & Swap
#Key: free-mem, free-ram, free-swap, total-swap
  def update_mem(self, key):
    lines = self.get_file_content_lines("/proc/meminfo")
    if lines:
      ram_free = self.process_meminfo(lines, ['Cached', 'MemFree', 'Buffers'])
      swap_total = self.process_meminfo(lines, ['SwapTotal'])
      swap_free = self.process_meminfo(lines, ['SwapCached', 'SwapFree'])
#      mem = self.process_meminfo(lines, ['Cached', 'MemFree', 'Buffers', 'SwapCached', 'SwapFree'])
      self.check_property_modified(['free-ram', ram_free], ['free-swap', swap_free], ['total-swap', swap_total], ['free-mem', ram_free + swap_free], ['total-mem', self.get_value('total-ram') + swap_total])
#      self.check_property_modified(['free-mem', self.get_value('free-ram') + self.get_value('free-swap')])
    self.add_timer_event(key)
    return False
#end

#Section: Free disk space
#Key: free-diskspace
  def update_free_diskspace(self, key):
    try:
      lines = self.get_shell_command_output("df | egrep '/$|/media' | awk {'print $6\" \"$4\" \"$3\" \"$2'} | sort").rsplit("\n")
      tmp = []
      names = []
      stats = []
      for x in lines:
        if x:
          data = x.rsplit(" ")
          tmp.append((data[0], long(data[1]), long(data[2]), long(data[3])))
      self.check_property_modified(['free-diskspace', tmp])
    except:
      pass
    self.add_timer_event(key)
    return False
#end

#Utility stuff
  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request', out_signature='s')
  def get_version(self):
    return self.version

  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request', out_signature='as')
  def get_property_list(self):
    return self.info_map.keys()

  @dbus.service.method(dbus_interface='ru.spirit.advanced_power_monitor.request', out_signature='v')
  def get_value(self, key):
    value = None
    if key in self.info_map:
      value = self.info_map[key]['value']
    return value

  def run_shell_command(self, cmd):
    if subprocess:
      subprocess.call(cmd, shell=True)
    else:
      os.system(cmd)

  def get_shell_command_output(self, cmd):
    result = ''
    if subprocess:
      result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    else:
      result = commands.getoutput(cmd)
    return result

  def set_value(self, key, value=None):
    self.info_map[key]['value'] = value

  def check_property_modified(self, *values):
    signals = []
    if values:
      for x in values:
        if self.get_value(x[0]) != x[1]:
          self.set_value(x[0], x[1])
          signals.append(x[0])
      if signals:
        self.notify(signals)

  def add_timer_event(self, key):
    if self.working and 'cb' in self.info_map[key] and 'time' in self.info_map[key]:
      self.info_map[key]['src_evt'] = gobject.timeout_add(self.info_map[key]['time'], self.info_map[key]['cb'], key)

  def get_file_content_lines(self, filename):
    lines = ""
    fd = None
    try:
      fd = open(filename, 'r')
    except:
      pass
    else:
      try:
        lines = fd.readlines()
      except:
        pass
      if fd:
        fd.close()
    return lines

  def process_meminfo(self, lines, filter_array):
    g = lambda x, v: x.find(v) != -1
    sum = 0
    for x in lines:
      for f in filter_array:
        if g(x, f):
          try:
            sum += long(x[0:x.rfind(' ')].replace(f+':', ''))
          except:
            pass
          break
    return sum
#end

#Testing section
#p = apm()
#p._cleanup()