'''
Created on Nov 18, 2010

@author: Wiberg-dude
'''
from network.server import Server
from network.client import Client
import pickle, socket, threading, time, SETTINGS

def serverStart(db):
    """
    Starts the networking server and listens for connections
    Needs a DatabaseWorker reference (db)
    """
    #Server(db).start()
    PingService().start()
    

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
        
        client_ip = '127.0.0.1'
        server_ip = SETTINGS.destination_ip
        employee_id = SETTINGS.employee_id
        print 'ska fixa pingpaketet'
        pingpaket = (employee_id, client_ip)
        print pingpaket
        print 'pingpaket fixat borja loopa'
        
        while True:
<<<<<<< HEAD
            print 'skickarrrrr'
            
            send(server_ip, pingpaket, 'ping')
            print 'skickat'
            time.sleep(10)
            
=======
            client_ip = socket.gethostbyname(socket.gethostname())
            server_ip = SETTINGS.destination_ip
            employee_id = SETTINGS.employee_id
            send(server_ip, pingpaket(client_ip, employee_id), 'ping')
            time.sleep(30)
>>>>>>> 48fd577f66bdb19d816deb7b567e79ac771def97
