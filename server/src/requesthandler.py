#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
from class_.base_objects import EmployeeStatus
#import SETTINGS
from db import Database
db = Database()

def request(data, type, e_id):
    import push
    #import network.networkcomponent as networkcomponent
    """
    Does different things depending on the datatype-object
    """
    print 'request starts!'
    if (type == 'db_add_or_update'): #Updating database
        print 'type = db_add_or_update'
        db.add_or_update(data)
        push.add(data, e_id)
    
    elif (type == 'ping'):
        print 'type = ping'
        print data

        e_status = db.get_one_by_id(EmployeeStatus, e_id)
        print "Tagit emot pingpaket från employee-id: %s" % (e_status.e_id)
        e_status.online = True
        e_status.ip = data
        print e_status
        db.commit()
        db.add_or_update(e_status)
        
        print 'uppdaterat databasen'