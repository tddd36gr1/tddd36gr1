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
from threading import Lock

class Database():
    
    class __impl(threading.Thread):
        """
        This should be the only object having direct access with the database.
        """
        lock = Lock()

        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
            #Initializing database by opening MySQL-database
            #and creating a new SQLAlchemy session
            global engine
            engine = create_engine(SETTINGS.db_src, encoding='utf-8')
            self.__Session = sessionmaker(bind=engine, autoflush=True, transactional=True)()
            base_objects.create_tables(engine)
            self.start()
    
        def add_all(self, objects):
            """
            Adds a list of objects into the database
            """
            self.lock.acquire()
            self.__Session.add_all(objects)
            self.__Session.commit()
            self.lock.release()
            
        def add(self, object):
            """
            Adds an object into the database
            """
            self.lock.acquire()
            self.__Session.add(object)
            self.__Session.commit()
            self.lock.release()
    
        def add_or_update(self, object):
            """
            
            Adds or updates the given object into the database depending
            if there already exists an object with same id or not.
            Used to merge unpickled objects received from the network
            """
            self.lock.acquire()
            result = self.__Session.merge(object)
            self.__Session.commit()
            self.lock.release()
            return result
            
        def get_all(self, object):
            """
            Returns a list of all objects of the same class as the parameter from database
            
            For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
            """
            self.lock.acquire()
            result = self.__Session.query(object).all()
            self.lock.release()
            return result
    
        def get_one(self, object):
            """
            Returns first object in database of the same class as the parameter
            
            For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
            """
            self.lock.acquire()
            result = self.__Session.query(object).first()
            self.lock.release()
            return result
        
        def commit(self):
            """
            Commits object changes to the database. Use this if you get an object from the database
            and then change some of its attributes
            """
            self.lock.acquire()
            self.__Session.commit()
            self.lock.release()
            
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
            self.lock.acquire()
            result = self.__Session.query(object).get(id)
            self.lock.release()
            return result
        
        def get_all_finished_missions(self):
            """
            Fetches all objects with finished status (3)
            """
            self.lock.acquire()
            result = self.__Session.query(Mission).filter_by(status=3).all()
            self.lock.release()
            return result
        
        def get_employee_by_name(self, name):
            """
            Fetches an employee with the name provided
            """
            self.lock.acquire()
            for employee in self.__Session.query(Employee).all():
                if (employee.fname+' '+employee.lname == name):
                    result = employee
            self.lock.release()
            return result
        
        def get_highest_device_id(self, object):
            self.lock.acquire()
            rows = self.__Session.query(object).filter(object.id<(SETTINGS.starting_id+1000)).filter(object.id>=SETTINGS.starting_id).all()
            if (len(rows) == 0):
                self.lock.release()
                return None
            result = rows[-1].id
            self.lock.release()
            return result
        
        def delete(self, object):
            self.lock.acquire()
            self.__Session.delete(object)
            self.__Session.commit()
            self.lock.release()

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Database.__instance is None:
            # Create and remember instance
            Database.__instance = Database.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = Database.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)