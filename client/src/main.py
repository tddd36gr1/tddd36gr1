'''
Created on 17 nov 2010

@author: Mandrill
'''
#coding=utf8

from db import DatabaseWorker
import network.networkcomponent as networkcomponent
import battery
import gui

db = DatabaseWorker()
battery.start()
networkcomponent.serverStart(db)
gui.start(db)