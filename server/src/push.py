#coding=utf8
from class_.base_objects import Mission, StatusCode, Employee, TextMessage
import network.networkcomponent as networkcomponent
import SETTINGS

def pushStart(db):
    """
    Starts pushing shit from database, yeh? Requires a motherf*ing DatabaseWorker
    """

    ip = SETTINGS.destination_ip
    
    testmsg = TextMessage('192.168.2.15', '192.168.2.15', 'Hej')
    networkcomponent.send(ip, testmsg, 'textMessage')
    
    #Send all status codes
    #print "StatusCodes"
    #for statuscode in db.get_all(StatusCode):
    #    networkcomponent.send(ip,statuscode,'db_add_or_update')
    #    print statuscode
    
    #Send all missions
    #print "Missions"
    #for mission in db.get_all(Mission):
    #    networkcomponent.send(ip,mission,'db_add_or_update')
    #    print mission
    
    #Send all employees
    #print "Employees"
    #for employee in db.get_all(Employee): 
    #    networkcomponent.send(ip,employee,'db_add_or_update')
    #    print employee