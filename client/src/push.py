#coding=utf8
from class_.base_objects import *
import SETTINGS, Queue, gui, gtk, db, threading
import network.networkcomponent as networkcomponent

db = db.database
q = Queue.Queue()
Qdone = Queue.Queue()
Qerrors = Queue.Queue()


def queuePusher():

    while 1:
        
        row = q.get()
        print row

        if (row.tablename == "missions"):
            object = db.get_one_by_id(Mission, row.object_id)
        elif (row.tablename == "statuscodes"):
            object = db.get_one_by_id(StatusCode, row.object_id)
        elif (row.tablename == "employees"): 
            object = db.get_one_by_id(Employee, row.object_id)
        elif (row.tablename == "text_message"):
            object = db.get_one_by_id(TextMessage, row.object_id)
        elif (row.tablename == "missiontexts"):
            object = db.get_one_by_id(MissionText, row.object_id)
        elif (row.tablename == "missionimages"):
            object = db.get_one_by_id(MissionImage, row.object_id)
        elif (row.tablename == "placemark"):
            object = db.get_one_by_id(Placemark, row.object_id)

        networkcomponent.send(SETTINGS.destination_ip, object, "db_add_or_update")
     #   try:
     #       networkcomponent.send(SETTINGS.ip_destination, object, "db_add_or_update")
     #   except:
    #        print "Fail from push"
   #         gtk.gdk.threads_enter()
  #          gui.notify_connection(False)
 #           gtk.gdk.threads_leave()
#            q.put(row)
#        else:
#            Qdone.put(row)
#            q.task_done()
            
def add(object):
        print "PushAdd"
        row = QueueRow(object.__tablename__, object.id)
        db.add_or_update_no_push(row)
        print "Queuerow added to queue"
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