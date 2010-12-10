#coding=utf8
import db
from class_.base_objects import *
import network.networkcomponent as networkcomponent
import SETTINGS
import Queue
import threading

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
            db.add_or_update(QueueRow(e.id, "Mission", o.id))
        
        for o in db.get_all(StatusCode):
            db.add_or_update(QueueRow(e.id, "StatusCode", o.id))
            
        for o in db.get_all(Employee):
            db.add_or_update(QueueRow(e.id, "Employee", o.id))
        
        #Special for text messages, only send if employee is receiver or sender    
        for o in db.get_all(TextMessage):
            if (e.id == o.src) or (e.id == o.dst):
                db.add_or_update(QueueRow(e.id, "TextMessage", o.id))
          
        for o in db.get_all(MissionText):
            db.add_or_update(QueueRow(e.id, "MissionText", o.id))
        
        for o in db.get_all(MissionImage):
            db.add_or_update(QueueRow(e.id, "MissionImage", o.id))
            
        for o in db.get_all(Placemark):
            db.add_or_update(QueueRow(e.id, "Placemark", o.id))

class QueuePusher(threading.Thread):
    def __init__(self, employee):
        threading.Thread.__init__ ( self )
        self.employee = employee
        self.q = Qlist[employee.id]
        
    def run(self):
        while 1:
            row = self.q.get()
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

            print object
            self.q.task_done()

def add(object):
    return
    

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