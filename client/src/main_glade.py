'''
Created on 17 nov 2010

@author: Mandrill
'''
#coding=utf8

from db import DatabaseWorker
#import networkcomponentnossl as networkcomponent
import glade_test as gui
import threading

db = DatabaseWorker()
#networkcomponent.serverStart(db)
threading.Thread(target=gui.start(db)).start()
