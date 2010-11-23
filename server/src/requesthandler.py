#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import network.networkcomponent
from class_.base_objects import TextMessage

def request(data, type, db):
    print 'request starts!'
    if (type == 'db_add_or_update'):
        print 'type correct'
        db.add_or_update(data)
    elif (type == 'textMessage'):
        txtmsg = data
        networkcomponent.send(txtmsg.dst, txtmsg, 'textMessage')