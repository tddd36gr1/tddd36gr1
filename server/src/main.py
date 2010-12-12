#coding=utf8
import push
import threading
import network.networkcomponent as networkcomponent

#push.populateQueue()
networkcomponent.serverStart()
print "Server is running"
threading.Thread(target=push.pushStart())