# coding=utf8
'''
Created on 8 nov 2010

@author: linus
'''

import socket
import threading
import time


# 
class Threadednetwork(threading.Thread):

    def __init__(self,conn,addr):
        self.conn = conn
        self.addr = addr
        threading.Thread.__init__ ( self )
        
    def run(self):
        #skriver ut anslutningen
        #print 'Connected by', self.addr
        #tar emot data
        data = self.conn.recv(1024)
        #splitar datat
        spliteddata = data.split('<>')
        data = spliteddata[0]
        datatype = spliteddata[1]

        #skrev ut datan förut
        #print data+' '+datatype
        self.conn.close()

#     
class NetworkServer(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__ ( self )
    
    def run(self):
        
        #set up the server
        HOST = ''                 # Tar emot alla mojliga anslutningar
        PORT = 50011              # Valjer en port
        
        # Oppnar socketanslutningen
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)
                
        while True:
            conn, addr = s.accept()
            Threadednetwork(conn, addr).start()    


    
#funktion for att starta igang servern
def serverStart():
    NetworkServer().start()


# funktion for att skicka data over natverket
def send(destination,package,type):
    HOST = destination    # The remote host
    PORT = 50011          # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    paket=package+'<>'+type
    s.send(paket)
    #data = s.recv(1024)
    s.close()
    #print 'Received', repr(data)
    
