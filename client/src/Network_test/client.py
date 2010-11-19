from OpenSSL import SSL
import sys, os, select, socket

class Client():
    
    global verify_cb
    
    def __init__(self, destination):
        self.destination = destination
    
    def verify_cb(conn, cert, errnum, depth, ok):
        # This obviously has to be updated
        print 'Got certificate: %s' % cert.get_subject()
        return ok
    
    def clientStart(self):
        HOST = self.destination
        PORT = 5039
        
        # Initialize context
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.set_verify(SSL.VERIFY_PEER, verify_cb) # Demand a certificate
        ctx.use_privatekey_file ('client.pkey')
        ctx.use_certificate_file('client.cert')
        ctx.load_verify_locations('CA.cert')
        
        # Set up client
        global sock
        sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sock.connect((HOST, PORT))
        
        
    def send(self, msg):
        try:
            sock.send(msg)
        except SSL.Error:
            print 'Connection died unexpectedly'
            return
        
    def close(self):
        sock.shutdown()
        sock.close()
        
        