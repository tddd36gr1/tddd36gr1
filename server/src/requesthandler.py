#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import db

def request(data, type):
    print 'request starts!'
    if (type == 'db_add_or_update'):
        print 'type correct'
        db.lock.acquire()
        db.add_or_update(data)
        db.lock.release()
    
