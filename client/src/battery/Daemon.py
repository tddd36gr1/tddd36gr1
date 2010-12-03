'''
Abstract Daemon
2009(c) Kiril Plyashkevich <ru.spirit@gmail.com>
Class for creating daemons.
'''
import sys, os, time, atexit
from signal import SIGTERM

class AbstractDaemon():
  def __init__(self, pidfile='/tmp/abstract_daemon.pid', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    self.stdin = stdin
    self.stdout = stdout
    self.stderr = stderr
    self.pidfile = pidfile

  def daemonize(self):
    try: 
      pid = os.fork() 
      if pid > 0:
        sys.exit(0) 
    except OSError, e:
      print e
      sys.stderr.write("Fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
      sys.exit(1)

    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    try: 
      pid = os.fork() 
      if pid > 0:
        sys.exit(0) 
    except OSError, e: 
      print e
      sys.stderr.write("Fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
      sys.exit(1) 

    sys.stdout.flush()
    sys.stderr.flush()
    si = file(self.stdin, 'r')
    so = file(self.stdout, 'a+')
    se = file(self.stderr, 'a+', 0)
#    os.dup2(si.fileno(), sys.stdin.fileno())
#    os.dup2(so.fileno(), sys.stdout.fileno())
#    os.dup2(se.fileno(), sys.stderr.fileno())

    atexit.register(self.delpid)
    pid = str(os.getpid())
    pidf = file(self.pidfile,'w+')
    pidf.write("%s\n" % pid)
    pidf.close()

  def delpid(self):
    os.remove(self.pidfile)

  def start(self):
    pid = self.get_pid()
    if pid:
      message = "File %s already exist. Daemon already running?\n"
      sys.stderr.write(message % self.pidfile)
      sys.exit(1)
    self.daemonize()
    self.run()

  def stop(self):
    pid = self.get_pid()

    if not pid:
      message = "File %s does not exist. Daemon not running?\n"
      sys.stderr.write(message % self.pidfile)
      return

    try:
      while 1:
        os.kill(pid, SIGTERM)
        time.sleep(0.1)
    except OSError, err:
      err = str(err)
      if err.find("No such process") > 0:
        if os.path.exists(self.pidfile):
          os.remove(self.pidfile)
      else:
        print str(err)
        sys.exit(1)

  def restart(self):
    self.stop()
    self.start()

  def get_pid(self):
    pid = None
    try:
      pf = file(self.pidfile,'r')
      pid = int(pf.read().strip())
      pf.close()
    except IOError:
      pass
    return pid

  def run(self):
    pass