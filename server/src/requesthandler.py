#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import db

def request(data, type):
    if (type == 'db_add_or_update'):
        db.add_or_update(data)
    
