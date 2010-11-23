#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
import network.networkcomponent

def request(data, type, db):
    """
    Does different things depending on the datatype-object
    """
    print 'request starts!'
    if (type == 'db_add_or_update'): #Updating database
        print 'type = db_add_or_update'
        db.add_or_update(data)
        networkcomponent.send(SETTINGS.secondary_ip, data, type) #Updating the second server
    elif (type == 'textMessage'): #Sending message
        print 'type = textMessage'
        txtmsg = data
        network.networkcomponent.send(txtmsg.dst, txtmsg, 'textMessage')