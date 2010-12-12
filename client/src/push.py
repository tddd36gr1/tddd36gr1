#coding=utf8
from class_.base_objects import Mission, StatusCode, Employee, TextMessage
import SETTINGS, Queue

db = db.database
q = Queue.Queue()
Qdone = Queue.Queue()
Qerrors = Queue.Queue()


def fillQueue():
    import db
    db = db.database
    """
    Run this initially to fill up queue first time ever the system runs. Pushes out ALL relevant data to all employees
    """

    for o in db.get_all(Mission):
        db.add_or_update(QueueRow(o.__tablename__, o.id))
    
    for o in db.get_all(StatusCode):
        db.add_or_update(QueueRow(o.__tablename__, o.id))
        
    for o in db.get_all(Employee):
        db.add_or_update(QueueRow(o.__tablename__, o.id))
    
    #Special for text messages, only send if employee is receiver or sender    
    for o in db.get_all(TextMessage):
        if (e.id == o.src) or (e.id == o.dst):
            db.add_or_update(QueueRow(o.__tablename__, o.id))
      
    for o in db.get_all(MissionText):
        db.add_or_update(QueueRow(o.__tablename__, o.id))
    
    for o in db.get_all(MissionImage):
        db.add_or_update(QueueRow(o.__tablename__, o.id))
        
    for o in db.get_all(Placemark):
        db.add_or_update(QueueRow(o.__tablename__, o.id))

def queuePusher():
    while 1:
        row = q.get()

        if (row.class_name == "Mission"):
            object = db.get_one_by_id(Mission, row.object_id)
        elif (row.class_name == "StatusCode"):
            object = db.get_one_by_id(StatusCode, row.object_id)
        elif (row.class_name == "Employee"):
            object = db.get_one_by_id(Employee, row.object_id)
        elif (row.class_name == "TextMessage"):
            object = db.get_one_by_id(TextMessage, row.object_id)
        elif (row.class_name == "MissionText"):
            object = db.get_one_by_id(MissionText, row.object_id)
        elif (row.class_name == "MissionImage"):
            object = db.get_one_by_id(MissionImage, row.object_id)
        elif (row.class_name == "Placemark"):
            object = db.get_one_by_id(Placemark, row.object_id)

        try:
            networkcomponent.send(SETTINGS.ip_destination.ip, object, "db_add_or_update")
        except:
            print "Fail"
            
            q.put(row)
        else:
            Qdone.put(row)
            q.task_done()
    
def pushStart():
    """
    Starts pushing-loop, preferably, this is started as a thread
    """
    
    for row in db.get_all(QueueRow):
        q.put(row)
           
    threading.Thread(Target=queuePusher).start()     
    #QueuePusher().start()

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