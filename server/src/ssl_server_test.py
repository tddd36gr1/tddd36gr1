import socket
import ssl

HOST = ''                 # Tar emot alla mojliga anslutningar
PORT = 50014             # Valjer en port
        
        # Oppnar socketanslutningen
s = socket.socket()
s.bind((HOST, PORT))
s.listen(5)
    
while True:
    conn, addr = s.accept()
    sslconn = ssl.wrap_socket(conn,server_side=True,certfile="mycert.pem",keyfile="mycert.pem",ssl_version=ssl.PROTOCOL_TLSv1)
    print 'connection from', addr
            #Threadednetwork(conn, addr).start()   
    print sslconn.read()