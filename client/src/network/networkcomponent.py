'''
Created on Nov 18, 2010

@author: Wiberg-dude
'''
from network.server import Server
from network.client import Client
import pickle, socket, threading, time, SETTINGS

def serverStart():
    """
    Starts the networking server and listens for connections
    """
    Server().start()
    PingService().start()
    

def send(destination, data, datatype):
    """
    Sends data to a specific destination. For valid datatyp-strings, check requesthandler.py
    """
    print "Trying to send"
    client = Client(destination)
    client.clientStart()
    msg = pickle.dumps(data)+'<>'+datatype+'<>'+str(SETTINGS.employee_id)
    client.send(msg)
    client.close()


class PingService(threading.Thread):
    
    def run(self):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        client_ip = s.getsockname()
        
        client_ip2 = '130.236.76.110'
        server_ip = SETTINGS.destination_ip
        
        while True:
            print 'skickarrrrr'

            try:
                send(server_ip, client_ip2, 'ping')
            except:
                print "Fail'd to skick ping to serveh"
                gtk.gdk.threads_enter()
                gui.notify_connection(False)
                gtk.gdk.threads_leave()
                time.sleep(40)
            else:
                print 'skickat'
                time.sleep(55)
