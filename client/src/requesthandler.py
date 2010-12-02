#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import network.networkcomponent
from class_.base_objects import TextMessage
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
        print 'type: pong'
        
        """
        Recieves a list with ID
        """
        onlineLista = data
        
        """
        Updates whos online in db
        """
        for id in onlineLista:
            user = db.get_one_by_id(Employee, id)
            user.online = True
        db.commit()
        
        
