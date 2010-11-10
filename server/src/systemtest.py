#coding=utf8
'''
Created on Nov 9, 2010

@author: alek
'''
import db
from class_.base_objects import Employee
import networkcomponent

linus = Employee('SS:SS:SS:SS:SS:SS', 'Linus', 'Andersson')

#db.add(linus)

#networkcomponent.serverStart()
print linus
networkcomponent.send('130.236.217.2', linus, 'epic')