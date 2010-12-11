#coding=utf8
import db
from class_.base_objects import *
import network.networkcomponent as networkcomponent
import SETTINGS
import Queue
import threading
import time

db = db.database
Qlist = []
Qdone = Queue.Queue()
Qerrors = Queue.Queue()

def populateQueue():
    """
    Run this initially to fill up queue first time ever the system runs. Pushes out ALL relevant data to all employees
    """
    for e in db.get_all(Employee):
        for o in db.get_all(Mission):
            db.add_or_update(QueueRow(e.id, o.__tablename__, o.id))
        
        for o in db.get_all(StatusCode):
            db.add_or_update(QueueRow(e.id, o.__tablename__, o.id))
            
        for o in db.get_all(Employee):
            db.add_or_update(QueueRow(e.id, o.__tablename__, o.id))
        
        #Special for text messages, only send if employee is receiver or sender    
        for o in db.get_all(TextMessage):
            if (e.id == o.src) or (e.id == o.dst):
                db.add_or_update(QueueRow(e.id, o.__tablename__, o.id))
          
        for o in db.get_all(MissionText):
            db.add_or_update(QueueRow(e.id, o.__tablename__, o.id))
        
        for o in db.get_all(MissionImage):
            db.add_or_update(QueueRow(e.id, o.__tablename__, o.id))
            
        for o in db.get_all(Placemark):
            db.add_or_update(QueueRow(e.id, o.__tablename__, o.id))

class QueuePusher(threading.Thread):
    def __init__(self, employee):
        threading.Thread.__init__ ( self )
        self.employee = employee
        self.q = Qlist[employee.id]
        
    def run(self):
        while 1:
            # Om användaren är offline, vänta och försök igen
            if (self.employee.online == False):
                print self.employee.fname+" offline"
                time.sleep(5)
                continue    #Försök igen
            row = self.q.get()
            
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
            
            try:
                networkcomponent.send(self.employee.ip, object, "db_add_or_update")
            except:
                print "Fail"
                self.q.put(row)
                self.employee.online = False
                db.add_or_update(self.employee)
            else:
                Qdone.put(row)
                self.q.task_done()

def add(object, sender):
    for e in db.get_all(Employee):
        if (e == sender):
            continue
        row = QueueRow(e.id, object.__tablename__, object.id)
        db.add_or_update(row)
        Qlist[e.id].put(row)
        

def pushStart():
    """
    Starts pushing-loop, preferably, this is started as a thread
    """
    Qlist.append(Queue.Queue())
    
    for all in db.get_all(Employee):
        Qlist.append(Queue.Queue())
    
    for row in db.get_all(QueueRow):
        Qlist[row.e_id].put(row)
            
    for employee in db.get_all(Employee):
        QueuePusher(employee).start()

    while 1:
        if (Qdone.empty() != True):
            print "Task done!"
            db.delete(Qdone.get())