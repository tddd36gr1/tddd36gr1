'''
Created on Nov 11, 2010

@author: alek
'''
import network.networkcomponent as networkcomponent
from db import DatabaseWorker
db = DatabaseWorker()

networkcomponent.serverStart(db)