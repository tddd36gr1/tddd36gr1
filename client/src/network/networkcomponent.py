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
    Needs a DatabaseWorker reference (db)
    """
    Server().start()
    #PingService().start()
    

def send(destination, data, datatype):
    """
    Sends data to a specific destination. For valid datatyp-strings, check requesthandler.py
    """
    client = Client(destination)
    client.clientStart()
    msg = pickle.dumps(data)+'<>'+datatype
    client.send(msg)
    client.close()


class PingService(threading.Thread):
    
    def run(self):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        client_ip = s.getsockname()
        
        client_ip2 = '130.236.77.152'
        server_ip = SETTINGS.destination_ip
        employee_id = SETTINGS.employee_id
        print 'ska fixa pingpaketet'
        pingpaket = (employee_id, client_ip2)
        print pingpaket
        print 'pingpaket fixat borja loopa'
        
        while True:
            print 'skickarrrrr'
            send(server_ip, pingpaket, 'ping')
            print 'skickat'
            time.sleep(10)