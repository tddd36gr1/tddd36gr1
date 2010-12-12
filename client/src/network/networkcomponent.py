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
            send(server_ip, client_ip2, 'ping')
            print 'skickat'
            time.sleep(10)