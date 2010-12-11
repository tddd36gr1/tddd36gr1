'''
Created on 17 nov 2010

@author: Mandrill
'''
#coding=utf8

import network.networkcomponent as networkcomponent
import battery
import gui

battery.start()
networkcomponent.serverStart()
gui.start()