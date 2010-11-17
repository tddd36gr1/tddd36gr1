#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''

def request(data, type, db):
    print 'request starts!'
    if (type == 'db_add_or_update'):
        print 'type correct'
        db.add_or_update(data)