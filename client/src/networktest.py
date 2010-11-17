'''
Created on Nov 11, 2010

@author: alek
'''
import networkcomponentnossl as networkcomponent
from db import DatabaseWorker
db = DatabaseWorker()

networkcomponent.serverStart(db)