#coding=utf8
'''
Created on Nov 11, 2010

@author: alek
'''
from class_.base_objects import Employee
#import SETTINGS
import db
db = db.database

def request(data, type, employee):
    #import network.networkcomponent as networkcomponent
    """
    Does different things depending on the datatype-object
    """
    print 'request starts!'
    if (type == 'db_add_or_update'): #Updating database
        print 'type = db_add_or_update'
        db.add_or_update(data)
    
    elif (type == 'ping'):
        print 'type = ping'
        print data
        print 'då drar vi ner allt i databasen fifan'
        print data[1]

        employee = db.get_one_by_id(Employee, data[0])
        employee.online = True
        ip = data[1]
        employee.ip = ip
        print employee.ip
        ipfifan = str(employee.ip)
        print ipfifan
        db.commit()
        
        print 'uppdaterat databasen'
        
        onlineList = []
        
        for employee in db.get_all(Employee):
            print 'in i första loopen'
            if employee.online == True:
                print 'användaren är online'
                onlineList.append(employee.fname)
                
        
        print 'uppdaterat listan'
        
        print onlineList
        
        print 'skickar tillbaka en pong, fast denna funktion är avstängd.'
        
        #network.networkcomponent.send(ipfifan, onlineList, 'pong')
        print 'pongbajs skickat'
        
        """
        for employee in db.get_all(Employee):
            if employee.online == True:
                if employee.id != data[0]:
                    onlineList.append(employee.id)
        """
        
        #send(employee.ip,onlineList,'pong')
