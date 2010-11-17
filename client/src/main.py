'''
Created on 10 nov 2010

@author: linus
'''

import gui_views
from gui_views import *
from db import DatabaseWorker
import networkcomponentnossl as networkcomponent

db = DatabaseWorker()
networkcomponent.serverStart(db)
gui_views.HalloWorldApp()
#Linus testar: gui_views_test2.HelloWorldApp()
print 'troloolololo'