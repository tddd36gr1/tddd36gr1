#coding=utf8

from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine
from class_ import base_objects
from threading import Lock
import SETTINGS

#Initializing database by opening MySQL-database
#and creating a new SQLAlchemy session
engine = create_engine(SETTINGS.db_src, encoding='utf-8')
Session = sessionmaker(bind=engine, autoflush=True, transactional=True)
base_objects.create_tables(engine)
lock = Lock()

def add_all(objects):
    """
    Adds a list of objects into the database
    """
    lock.acquire()
    session = Session()
    session.save_all(objects)
    session.commit()
    session.close()
    lock.acquire()

def add(object):
    """
    Adds an object into the database
    """
    lock.acquire()
    session = Session()
    session.save(object)
    session.commit()
    session.close()
    lock.acquire()
    
def get_all(object):
    """
    Returns a list of all objects of the same class as the parameter from database
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    lock.acquire()
    session = Session()
    return session.query(object).all()
    session.close()
    lock.acquire()

def get_one(object):
    """
    Returns first object in database of the same class as the parameter
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    lock.acquire()
    session = Session()
    return session.query(object).first()
    session.close()
    lock.acquire()
    
def update(object):
    lock.acquire()
    session = Session()
    session.merge(object)
    session.commit()
    session.close()
    lock.release()
    
def add_or_update(object):
    session = Session()
    if (object.id == None):
        session.close()
        print "add"
        add(object)
    elif (session.query(object.__class__).get(object.id) != None):
        session.close()
        print "update"
        update(object)
    else:
        session.close()
        print "add"
        add(object)