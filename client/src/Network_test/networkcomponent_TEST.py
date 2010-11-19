'''
Created on Nov 18, 2010

@author: maemo
'''
from server import Server
from client import Client
import time
import threading
import pickle

def serverStart():
    server = Server().start()

def send(data, datatype, destination):
    client = Client(destination)
    client.clientStart()
    msg = pickle.dumps(data)+'<>'+datatype
    client.send(msg)
    client.close()
    
serverStart()
send('hej blah blah', 'db_add_or_update', '127.0.0.1')