# coding=utf8

'''
Created on 8 nov 2010

@author: linus und Mandrill
'''

import socket
import threading
import pickle
import requesthandler
import server, client

# startar upp trådar för varje mottaget paket
class Threadednetwork(threading.Thread):

    def __init__(self, conn, addr, db):
        self.db = db
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
        data = pickle.loads(data)
        datatype = spliteddata[1]

        #skrev ut datan förut
        print data.id
        requesthandler.request(data, datatype, self.db)
        self.conn.close()

# startar upp servern så att den ligger och lyssnar på anslutningar    
class NetworkServer(threading.Thread):
    
    def __init__(self, db):
        threading.Thread.__init__ ( self )
        self.db = db
    
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
            Threadednetwork(conn, addr, self.db).start()    

#funktion for att starta igang servern
def serverStart(db):
    NetworkServer(db).start()


# funktion for att skicka data over natverket
def send(destination,package,type):
    HOST = destination    # The remote host       # The same port as used by the server
    server.serverStart2()
    packat = pickle.dumps(package)
    package = packat+'<>'+type
    s.send(package)
    #data = s.recv(1024)
    s.close()
    print 'Received', repr(data)