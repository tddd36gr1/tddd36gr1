'''
Created on 5 nov 2010

@author: linus
'''
import socket

def send(destination,package):
    HOST = destination    # The remote host
    PORT = 50010              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    text = raw_input("Enter anything:")
    #s.send(text)
    s.send(text)
    data = s.recv(1024)
    s.close()
    print 'Received', repr(data)
    
send('130.236.77.47','hej')