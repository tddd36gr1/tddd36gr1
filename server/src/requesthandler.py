#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import network.networkcomponent

def request(data, type, db):
    print 'request starts!'
    if (type == 'db_add_or_update'):
        print 'type = db_add_or_update'
        db.add_or_update(data)
    elif (type == 'textMessage'):
        print 'type = textMessage'
        txtmsg = data
        network.networkcomponent.send(txtmsg.dst, txtmsg, 'textMessage')