'''
Created on 10 nov 2010

@author: linus
'''

<<<<<<< HEAD:client/src/main.py
#import gui_views
#from gui_views import *
import gui_views_test2
#from gui_views_test2 import *
#import threading
#from networkcomponent import *
import networkcomponent


networkcomponent.serverStart()
gui_views_test2.run()
=======
import gui_views
from gui_views import *
from db import DatabaseWorker
import networkcomponentnossl as networkcomponent

db = DatabaseWorker()
networkcomponent.serverStart(db)
gui_views.HalloWorldApp()
>>>>>>> ec0a1a19715034e53c7156dbde61eb8d133fa27f:client/src/main.py
#Linus testar: gui_views_test2.HelloWorldApp()
print 'troloolololo'