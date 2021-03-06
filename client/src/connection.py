import threading
import socket
import sys
import gtk
import gui
import time

class Connection_check(threading.Thread):

    def __init__(self):
        threading.Thread.__init__ ( self )
        self.connected = True
        
    def run(self):
        while 1:
            self.alert()
            time.sleep(55)
            
    
        
    def alert(self):
        #print >>sys.stderr, msg
        #sys.exit(1)
    
        (family, socktype, proto, garbage, address) = \
                socket.getaddrinfo("www.google.se", 80, 0, 0, socket.SOL_TCP)[0] # Use only the first tuple
        s = socket.socket(family, socktype, proto)
    
        try:
            (family, socktype, proto, garbage, address) = \
                socket.getaddrinfo("www.google.se", 80, 0, 0, socket.SOL_TCP)[0] # Use only the first tuple
            s = socket.socket(family, socktype, proto)
            
            
            s.connect(address)
            if (self.connected == False):
                self.connected = True
                gtk.gdk.threads_enter()
                gui.notify_connection(True)
                gtk.gdk.threads_leave()
            
        except Exception, e:
            #alert("Something's wrong with %s. Exception type is %s" % (address, e))
                self.connected = False
                gtk.gdk.threads_enter()
                gui.notify_connection(False)
                gtk.gdk.threads_leave()
                
    
def start():
    global check_connection
    check_connection = Connection_check()
    check_connection.start()
        