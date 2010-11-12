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
    session.add_all(objects)
    session.commit()
    session.close()
    lock.release()

def add(object):
    """
    Adds an object into the database
    """
    lock.acquire()
    print "Lock acquired"
    session = Session()
    session.add(object)
    session.commit()
    session.close()
    lock.release()
    print "Lock released"
    
def get_all(object):
    """
    Returns a list of all objects of the same class as the parameter from database
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    lock.acquire()
    print "Lock acquired"
    session = Session()
    result = session.query(object).all()
    session.close()
    lock.release()
    print "Lock released"
    return result
    
def get_one(object):
    """
    Returns first object in database of the same class as the parameter
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    lock.acquire()
    session = Session()
    result = session.query(object).first()
    session.close()
    lock.release()
    return result
    
def update(object):
    lock.acquire()
    session = Session()
    session.merge(object)
    session.commit()
    session.close()
    lock.release()
    
def add_or_update(object):
    lock.acquire()
    session = Session()
    id = session.query(object.__class__).get(object.id)
    session.close()
    lock.release()
    if (object.id == None):
        print "add"
        add(object)
    elif (id != None):
        print "update"
        update(object)
    else:
        print "add"
        add(object)