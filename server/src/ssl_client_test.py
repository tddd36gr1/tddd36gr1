import socket
import ssl
from OpenSSL import SSL

HOST = '127.0.0.1'
PORT = 50014

ctx = SSL.Context(SSL.TLSv1_METHOD)
s = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send('penis')
data = s.recv(1024)
print 'recieved', data
s.close()