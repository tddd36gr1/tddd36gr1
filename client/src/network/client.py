from OpenSSL import SSL
import sys, os, select, socket, SETTINGS

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
        PORT = SETTINGS.network_port_send
        
        # Initialize context, verify certificate
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.set_verify(SSL.VERIFY_PEER, verify_cb) #Ask for a certificate
        ctx.use_privatekey_file ('network/client.pkey')
        ctx.use_certificate_file('network/client.cert')
        ctx.load_verify_locations('network/CA.cert')
        
        #Starting client
        global sock
        print PORT
        print HOST
        sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        print 'sux'
        sock.connect((HOST, PORT))
        
        
    #Send
    def send(self, msg):
        try:
            sock.sendall(msg)
        except SSL.Error:
            pass
    #Close socket
    def close(self):
        sock.shutdown()
        sock.close()