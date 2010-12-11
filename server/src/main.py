#coding=utf8
import push
import threading
import network.networkcomponent as networkcomponent

push.populateQueue()
threading.Thread(target=push.pushStart())
networkcomponent.serverStart()