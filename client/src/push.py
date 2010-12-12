#coding=utf8
from class_.base_objects import *
import SETTINGS, Queue, gui, gtk, db, threading

db = db.database
q = Queue.Queue()
Qdone = Queue.Queue()
Qerrors = Queue.Queue()


def queuePusher():

    while 1:
        
        row = q.get()

        if (row.tablename == "Mission"):
            object = db.get_one_by_id(Mission, row.object_id)
        elif (row.tablename == "StatusCode"):
            object = db.get_one_by_id(StatusCode, row.object_id)
        elif (row.tablename == "Employee"):
            object = db.get_one_by_id(Employee, row.object_id)
        elif (row.tablename == "TextMessage"):
            object = db.get_one_by_id(TextMessage, row.object_id)
        elif (row.tablename == "MissionText"):
            object = db.get_one_by_id(MissionText, row.object_id)
        elif (row.tablename == "MissionImage"):
            object = db.get_one_by_id(MissionImage, row.object_id)
        elif (row.tablename == "Placemark"):
            object = db.get_one_by_id(Placemark, row.object_id)

        try:
            networkcomponent.send(SETTINGS.ip_destination, object, "db_add_or_update")
        except:
            print "Fail"
            gtk.gdk.threads_enter()
            gui.notify_connection(False)
            gtk.gdk.threads_leave()
            q.put(row)
        else:
            Qdone.put(row)
            q.task_done()
            
def add(object):
        row = QueueRow(object.__tablename__, object.id)
        db.add_or_update_no_push(row)
        q.put(row)
    
def pushStart():
    """
    Starts pushing-loop, preferably, this is started as a thread
    """
    
    for row in db.get_all(QueueRow):
        q.put(row)
           
    threading.Thread(target=queuePusher).start()
    threading.Thread(target=runDoneQueue).start()   
    #QueuePusher().start()


def runDoneQueue():
    while 1:
        if (Qdone.empty() != True):
            print "Task done!"
            db.delete(Qdone.get())

        
    

    
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