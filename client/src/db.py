# coding=utf8

from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine
from class_ import base_objects

#Initializing database by opening MySQL-database
#and creating a new SQLAlchemy session
engine = create_engine('sqlite:///db/n810.db')
Session = sessionmaker(bind=engine)
session = Session()
session.new
base_objects.create_tables(engine)


def add_all(objects):
    """
    Adds a list of objects into the database
    """
    session.add_all(objects)

def add(object):
    """
    Adds an object into the database
    """
    session.add(object)
    
def get_all(object):
    """
    Returns a list of all objects of the same class as the parameter from database
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    return session.query(object).all()

def get_one(object):
    """
    Returns first object in database of the same class as the parameter
    
    For more advanced queries, see http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_querying
    """
    return session.query(object).first()