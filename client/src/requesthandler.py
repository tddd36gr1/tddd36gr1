#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import network.networkcomponent
from class_.base_objects import *
import SETTINGS
import gui
import gtk.gdk
import pickle

def request(data, type, db):
    print 'request starts!'
    if (type == 'db_add_or_update'):
        print "type: db_add_or_update"
        db.add_or_update(data)
        gtk.gdk.threads_enter()
        gui.notify(data)
        gtk.gdk.threads_leave()
        
    elif (type == 'textMessage'):
        print "type: textMessage"
        msg = TextMessage(data.src, data.dst, data.msg)
        db.add_or_update(msg)
        gtk.gdk.threads_enter()
        gui.notify(msg)
        gtk.gdk.threads_leave()

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