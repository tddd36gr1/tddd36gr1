#!/usr/bin/env python
'''
Advanced Power Monitor Daemon
2009(c) Kirill Plyashkevich <ru.spirit@gmail.ru>
Works as daemon extending AbstractDaemon and creating Advanced Power Monitor.
'''
import sys, gobject
import Daemon
import AdvancedPowerMonitor

class apmd(Daemon.AbstractDaemon):
  def __init__(self):
    Daemon.AbstractDaemon.__init__(self, '/tmp/apmd.pid')
  
  def run(self):
    self.apm = AdvancedPowerMonitor.apm()
    gobject.MainLoop().run()

if __name__ == "__main__":
  daemon = apmd()
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      print 'Starting...'
      daemon.start()
    elif 'stop' == sys.argv[1]:
      print 'Stopping...'
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      print 'Restarting...'
      daemon.restart()
    else:
      print "Unknown command: %s" % sys.argv[1]
      print "Usage: %s start|stop|restart" % sys.argv[0]
      sys.exit(2)
    sys.exit(0)
  else:
    print "Usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)