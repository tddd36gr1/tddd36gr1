'''
Created on Nov 17, 2010

@author: Mandrill
'''
import threading
from sqlalchemy.orm import  sessionmaker, scoped_session
from sqlalchemy import create_engine
from class_ import base_objects
from class_.base_objects import *
import SETTINGS

class DatabaseWorker(threading.Thread):
    """
    This should be the only object having direct access with the database.
    Note that there can only be ONE instance of this class. In order to use it in different components,
    main should create the one and only instance of DatabaseWorker and pass a reference to each other component
    needing to use the database.
    
    Example main.py:
    from db import DatabaseWorker
    import push
    
    db = DatabaseWorker()
    #PASS THIS VARIABLE TO OTHER CLASSES!!!!
    
    push.pushStart(db)
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        #Initializing database by opening MySQL-database
        #and creating a new SQLAlchemy session
        global engine
        engine = create_engine(SETTINGS.db_src, encoding='utf-8')
        self.__Session = scoped_session(sessionmaker(bind=engine, autoflush=True, transactional=True))
        base_objects.create_tables(engine)
        self.start()

    def add_all(self, objects):
        """
        Adds a list of objects into the database
        """
        self.__Session.add_all(objects)
        self.__Session.commit()
        
    def add(self, object):
        """
        Adds an object into the database
        """
        self.__Session.add(object)
        self.__Session.commit()

    def add_or_update(self, object):
        """
        Adds or updates the given object into the database depending
        if there already exists an object with same id or not.
        Used to merge unpickled objects received from the network
        """
        result = self.__Session.merge(object)
        self.__Session.commit()
        return result
        
    def get_all(self, object):
        """
        Returns a list of all objects of the same class as the parameter from database
        
        For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
        """
        return self.__Session.query(object).all()

    def get_one(self, object):
        """
        Returns first object in database of the same class as the parameter
        
        For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
        """
        return self.__Session.query(object).first()
    
    def commit(self):
        """
        Commits object changes to the database. Use this if you get an object from the database
        and then change some of its attributes
        """
        self.__Session.commit()
        
    def get_session(self):
        """
        Returns the database worker's Session-object, use at own discretion :O
        """
        return self.__Session
    
    def get_one_by_id(self, object, id):
        """
        Fetches an object from database with a matching id
        Example: get_one_by_id(Employee, 2) returns the employee object with id == 2
        """
        return self.__Session.query(object).get(id)
    
    def get_all_finished_missions(self):
        """
        Fetches all objects with finished status (3)
        """
        return self.__Session.query(Mission).filter_by(status=3).all()
    
    def get_employee_by_name(self, name):
        """
        Fetches an employee with the name provided
        """
        for employee in self.__Session.query(Employee).all():
            if (employee.fname+' '+employee.lname == name):
                return employee
        return
    
    def get_highest_device_id(self, object):
        rows = self.__Session.query(object).filter(object.id<(SETTINGS.starting_id+999)).filter(object.id>=SETTINGS.starting_id).all()
        if (len(rows) == 0):
            return None
        return rows[-1].id
    
    def get_all_users_online(self):
        return self.__Session.query(Employee).filter_by(online=True).all()

database = DatabaseWorker()