'''
Created on Nov 18, 2010

@author: maemo
'''
from network_test.server import Server
from network_test.client import Client
from class_.base_objects import StatusCode
import time
import threading
import pickle

def serverStart(db):
    """
    Starts the networking server and listens for connections
    Needs a DatabaseWorker reference (db)
    """
    server = Server(db).start()

def send(data, datatype, destination):
    """
    Sends data to a specific destination. For valid datatyp-strings, check requesthandler.py
    """
    client = Client(destination)
    client.clientStart()
    msg = pickle.dumps(data)+'<>'+datatype
    client.send(msg)
    client.close()