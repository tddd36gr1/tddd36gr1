#coding=utf8
from class_.base_objects import *
import network.networkcomponent as networkcomponent
import SETTINGS

def pushStart(db):
    """
    Starts pushing shit from database, yeh? Requires a motherf*ing DatabaseWorker
    """

    ip = SETTINGS.destination_ip
    
    #testmsg = TextMessage('192.168.2.15', '192.168.2.15', 'Hej')
    #networkcomponent.send(ip, testmsg, 'textMessage')
    
    #Send all status codes
    print "Status codes"
    for statuscode in db.get_all(StatusCode):
        networkcomponent.send(ip,statuscode,'db_add_or_update')
        print statuscode
    
    #Send all missions
    print "Missions"
    for mission in db.get_all(Mission):
        networkcomponent.send(ip,mission,'db_add_or_update')
        print mission
    
    #Send all employees
    print "Employees"
    for employee in db.get_all(Employee): 
        networkcomponent.send(ip,employee,'db_add_or_update')
        print employee
        
    #Send all mission images
    print "Mission images"
    for image in db.get_all(MissionImage):
        networkcomponent.send(ip, image, 'db_add_or_update')
        
    #Send all mission texts
    print "Mission texts"
    for text in db.get_all(MissionText):
        networkcomponent.send(ip, text, 'db_add_or_update')
        
    #Send all text messages
    print "Text messages"
    for msg in db.get_all(TextMessage):
        networkcomponent.send(ip, msg, 'textMessage')