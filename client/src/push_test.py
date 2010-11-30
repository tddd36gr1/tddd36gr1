#coding=utf8
'''
Created on Nov 23, 2010

@author: alek
'''

import push
from db import DatabaseWorker

db = DatabaseWorker()
push.pushStart(db)