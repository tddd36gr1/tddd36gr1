from OpenSSL import SSL
import sys, os, select, socket
import threading
import pickle
import requesthandler, SETTINGS

class Server(threading.Thread):
    
    global verify_cb
    global server
    global dropClient
    
    #Verifyingfunction, not complete
    def verify_cb(conn, cert, errnum, depth, ok):
        print 'Got certificate: %s' % cert.get_subject()
        return ok
    
    def __init__(self):
        threading.Thread.__init__ ( self )
        
    def run(self):
        # Initialize context, verify certificate
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.set_options(SSL.OP_NO_SSLv2)
        ctx.set_verify(SSL.VERIFY_PEER|SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify_cb) #Ask for a certificate
        ctx.use_privatekey_file ('network/server.pkey')
        ctx.use_certificate_file('network/server.cert')
        ctx.load_verify_locations('network/CA.cert')
        
        # Starting server, open socket
        server = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        server.bind(('', SETTINGS.network_port))
        server.listen(3) 
        server.setblocking(0)
        
        global clients
        clients = {}
        global writers
        writers = {}
        
        while 1:
            try:
                r,w,_ = select.select([server]+clients.keys(), writers.keys(), [])
            except:
                break
        
            for cli in r:
                if cli == server:
                    #Accepting the connection from server
                    cli,addr = server.accept()
                    print 'Connection from %s' % (addr,)
                    clients[cli] = addr
        
                else:
                    try:
                        #Receieving data, spliting, unpickle..
                        ret = cli.recv(8192)
                        spliteddata = ret.split('<>')
                        data = spliteddata[0]
                        data = pickle.loads(data)
                        datatype = spliteddata[1]
                        
                        #forwarding data to requesthandler
                        requesthandler.request(data, datatype)
                        
                    except (SSL.WantReadError, SSL.WantWriteError, SSL.WantX509LookupError):
                        pass
                    except SSL.ZeroReturnError:
                        dropClient(cli)
                    except SSL.Error, errors:
                        dropClient(cli, errors)
                    else:
                        if not writers.has_key(cli):
                            writers[cli] = ''
                        writers[cli] = writers[cli] + ret

        for cli in clients.keys():
            cli.close()
        server.close()
        
    #Client disconnect if errors appear
    def dropClient(cli, errors=None):
        if errors:
            print 'Client %s left unexpectedly:' % (clients[cli],)
            print '  ', errors
        else:
            print 'Client %s left politely' % (clients[cli],)
        del clients[cli]
        if writers.has_key(cli):
            del writers[cli]
        if not errors:
            cli.shutdown()
        cli.close()