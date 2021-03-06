from OpenSSL import SSL
import sys, os, select, socket, SETTINGS

class Client():
    
    global verify_cb
    
    def __init__(self, destination):
        self.destination = destination
    
    #Verifyingfunction, not complete
    def verify_cb(conn, cert, errnum, depth, ok):
        return ok
    
    def clientStart(self):
        HOST = self.destination
        PORT = SETTINGS.network_port_send
        
        # Initialize context, verify certificate
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.set_verify(SSL.VERIFY_PEER, verify_cb) #Ask for a certificate
        ctx.use_privatekey_file ('network/client.pkey')
        ctx.use_certificate_file('network/client.cert')
        ctx.load_verify_locations('network/CA.cert')
        
        #Starting client
        global sock
        sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock.connect((HOST, PORT))
        
    #Send
    def send(self, msg):
        try:
            sock.sendall(msg)
        except:
            pass
#        except SSL.Error:
#            print 'Connection died unexpectedly'
#            return
    #Close socket
    def close(self):
        sock.shutdown()
        sock.close()