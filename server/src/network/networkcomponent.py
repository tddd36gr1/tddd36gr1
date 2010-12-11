'''
Created on Nov 18, 2010

@author: Wiberg-dude
'''
from network.server import Server
from network.client import Client
import pickle
from threading import Lock

lock = Lock()

def serverStart():
    """
    Starts the networking server and listens for connections
    """
    Server().start()
    #send('127.0.0.1','lol','TextMessage')

def send(destination, data, datatype):
    """
    Sends data to a specific destination. For valid datatyp-strings, check requesthandler.py
    """
    msg = pickle.dumps(data)+'<>'+datatype
    lock.acquire()
    client = Client(destination)
    try:
        client.clientStart()
        print "Client started"
        client.send(msg)
        print "Client sent"
        client.close()
        lock.release()
    except:
        lock.release()
        raise