#coding=utf8

from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine
from class_ import base_objects

#Initializing database by opening MySQL-database
#and creating a new SQLAlchemy session
engine = create_engine('mysql://pythonserver:tddd36gr1@localhost/pythonserver', encoding='utf-8')
Session = sessionmaker(bind=engine, autocommit=True, transactional=True)
base_objects.create_tables(engine)


def add_all(objects):
    """
    Adds a list of objects into the database
    """
    session = Session()
    session.add_all(objects)
    session.close()

def add(object):
    """
    Adds an object into the database
    """
    session = Session()
    session.add(object)
    session.close()
    
def get_all(object):
    """
    Returns a list of all objects of the same class as the parameter from database
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    session = Session()
    return session.query(object).all()
    session.close()

def get_one(object):
    """
    Returns first object in database of the same class as the parameter
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    session = Session()
    return session.query(object).first()
    session.close()