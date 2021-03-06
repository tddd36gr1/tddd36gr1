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
        server.bind(('', SETTINGS.network_port_receive))
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
                    clients[cli] = addr
        
                else:
                    try:
                        #Receieving data, spliting, unpickle..
                        ret = cli.recv(102400)
                        spliteddata = ret.split('<>')
                        data = spliteddata[0]
                        data = pickle.loads(data)
                        datatype = spliteddata[1]
                        employee_id = spliteddata[2]
                        
                        #forwarding data to requesthandler
                        requesthandler.request(data, datatype, employee_id)
                        
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
        del clients[cli]
        if writers.has_key(cli):
            del writers[cli]
        if not errors:
            cli.shutdown()
        cli.close()