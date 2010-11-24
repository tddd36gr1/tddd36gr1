'''
Created on 10 nov 2010

@author: linus
'''

from db import DatabaseWorker
import networkcomponentnossl as networkcomponent
import gui_MANDRILL as gui
import threading

db = DatabaseWorker()
networkcomponent.serverStart(db)
threading.Thread(target=gui.start(db)).start()
