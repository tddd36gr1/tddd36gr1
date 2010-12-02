#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import network.networkcomponent
from class_.base_objects import *
import SETTINGS

def request(data, type, db):
    print 'request starts!'
    if (type == 'db_add_or_update'):
        print "type: db_add_or_update"
        db.add_or_update(data)
        
    elif (type == 'textMessage'):
        print "type: textMessage"
        db.add_or_update(TextMessage(data.src, data.dst, data.msg))

    elif (type == 'pong'):
        """
        Recieves a list with ID
        """
        print 'type: pong'
        onlineLista = data
        
        """
        Updates whos online in db
        """
        for id in onlineLista:
            user = db.get_one_by_id(Employee, id)
            user.online = True
        db.commit()
        
def send_message(textmessage, db):
    print "Send_request"
    db.add_or_update(textmessage)
    textmessage.src_object = db.get_one_by_id(Employee, textmessage.src)
    textmessage.dst_object = db.get_one_by_id(Employee, textmessage.dst)
    db.commit()
    #networkcomponent.send(SETTINGS.)