from OpenSSL import SSL
import sys, os, select, socket

class Client():
    
    global verify_cb
    
    def __init__(self, destination):
        self.destination = destination
    
    #Verifyingfunction, not complete
    def verify_cb(conn, cert, errnum, depth, ok):
        print 'Got certificate: %s' % cert.get_subject()
        return ok
    
    def clientStart(self):
        HOST = self.destination
        PORT = 5040
        
        # Initialize context, verify certificate
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.set_verify(SSL.VERIFY_PEER, verify_cb) #Ask for a certificate
        ctx.use_privatekey_file ('network_test/client.pkey')
        ctx.use_certificate_file('network_test/client.cert')
        ctx.load_verify_locations('network_test/CA.cert')
        
        #Starting client
        global sock
        sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock.connect((HOST, PORT))
        
    #Send
    def send(self, msg):
        try:
            sock.send(msg)
        except SSL.Error:
            print 'Connection died unexpectedly'
            return
    #Close socket
    def close(self):
        sock.shutdown()
        sock.close()
        
        