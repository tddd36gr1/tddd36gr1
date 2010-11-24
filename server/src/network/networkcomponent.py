'''
Created on Nov 18, 2010

@author: Wiberg-dude
'''
from network.server import Server
from network.client import Client
import pickle

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
    
        