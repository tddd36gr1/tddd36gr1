#coding=utf8
import push
import threading

#push.populateQueue()
threading.Thread(target=push.pushStart())