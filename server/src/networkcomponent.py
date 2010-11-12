# coding=utf8

'''
Created on 8 nov 2010

@author: linus <3 wiberg
'''

import socket
import threading
import time
import pickle
import ssl
from OpenSSL import SSL
#import requesthandler


# startar upp trådar för varje mottaget paket
class Threadednetwork(threading.Thread):

    def __init__(self,conn,addr,data):
        self.conn = conn
        self.addr = addr
        self.data = data
        threading.Thread.__init__ ( self )
        
    def run(self):
        #skriver ut anslutningen
        print 'Connected by', self.addr
        #splittar datat
        spliteddata = self.data.split('<>')
        data = spliteddata[0]
        data = pickle.loads(self.data)
        datatype = spliteddata[1]
        #skrev ut datan förut
        print data
        print 'connection closed', self.addr
        
        #requesthandler.request(data, datatype)
        self.conn.close()

# startar upp servern så att den ligger och lyssnar på anslutningar    
class NetworkServer(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__ ( self )
    
    def run(self):
        
        #set up the server
        HOST = ''                 # Tar emot alla mojliga anslutningar
        PORT = 50011              # Valjer en port
        
        # Oppnar socketanslutningen
        s = socket.socket()
        s.bind((HOST, PORT))
        s.listen(5)
    
        while True:
            conn, addr = s.accept()
            sslconn = ssl.wrap_socket(conn,server_side=True,certfile="mycert.pem",keyfile="mycert.pem",ssl_version=ssl.PROTOCOL_TLSv1)
            data = sslconn.read()
            Threadednetwork(conn, addr, data).start()   
          
    
#funktion for att starta igang servern
def serverStart():
    NetworkServer().start()


# funktion for att skicka data over natverket
def send(destination,package,type):
    HOST = destination    # The remote host
    PORT = 50011          # The same port as used by the server
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSSL = SSL.Context(SSL.TLSv1_METHOD)
    s = SSL.Connection(clientSSL, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    s.connect((HOST, PORT))
    Picklatpaket = pickle.dumps(package)
    paket = Picklatpaket+'<>'+type
    s.send(paket)
    s.close()