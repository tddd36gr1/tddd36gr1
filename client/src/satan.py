import socket
import sys

def alert(msg):
    print >>sys.stderr, msg
    sys.exit(1)

(family, socktype, proto, garbage, address) = \
         socket.getaddrinfo("www.google.se", 80, 0, 0, socket.SOL_TCP)[0] # Use only the first tuple
s = socket.socket(family, socktype, proto)

try:
    s.connect(address)
    print("Du har en internetanslutning")
except Exception, e:
    #alert("Something's wrong with %s. Exception type is %s" % (address, e))
    print("Du har INTE en internetanslutning")