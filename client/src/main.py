'''
Created on 17 nov 2010

@author: Mandrill
'''
#coding=utf8

import network.networkcomponent as networkcomponent
import battery
import gui
import connection
import push

battery.start()
connection.start()
networkcomponent.serverStart()
push.pushStart()
gui.start()
