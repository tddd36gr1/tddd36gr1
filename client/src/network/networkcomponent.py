'''
Created on Nov 18, 2010

@author: Wiberg-dude
'''
from network.server import Server
from network.client import Client
import pickle, socket, SETTINGS, threading, time

def serverStart(db):
    """
    Starts the networking server and listens for connections
    Needs a DatabaseWorker reference (db)
    """
    Server(db).start()

def send(destination, data, datatype):
    """
    Sends data to a specific destination. For valid datatyp-strings, check requesthandler.py
    """
    client = Client(destination)
    client.clientStart()
    msg = pickle.dumps(data)+'<>'+datatype
    client.send(msg)
    client.close()

class PingPaket():

    def __init__():
        ip = socket.gethostbyname(socket.gethostname())
        id = SETTINGS.employee_id

class PingService(threading.tread):
    
    def run(self):
        
        while True:
            client_ip = socket.gethostbyname(socket.gethostname())
            server_ip = SETTINGS.destination_ip
            employee_id = SETTINGS.employee_id
            send(server_ip, pingpaket(client_ip, employee_id), 'ping')
            time.sleep(30)
            
