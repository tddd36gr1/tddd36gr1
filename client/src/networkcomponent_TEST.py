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

from db import DatabaseWorker

db = DatabaseWorker()

def serverStart():
    server = Server(db).start()

def send(data, datatype, destination):
    client = Client(destination)
    client.clientStart()
    msg = pickle.dumps(data)+'<>'+datatype
    client.send(msg)
    client.close()
    
serverStart()

send(StatusCode("Brunka"), 'db_add_or_update', '127.0.0.1')