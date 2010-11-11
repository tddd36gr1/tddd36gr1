#coding=utf8

from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine
from class_ import base_objects

#Initializing database by opening MySQL-database
#and creating a new SQLAlchemy session
engine = create_engine('sqlite:///db/n810.db', encoding='utf-8')
Session = sessionmaker(bind=engine, autoflush=True, transactional=True)
base_objects.create_tables(engine)


def add_all(objects):
    """
    Adds a list of objects into the database
    """
    session = Session()
    session.save_all(objects)
    session.commit()
    session.close()

def add(object):
    """
    Adds an object into the database
    """
    session = Session()
    session.save(object)
    session.commit()
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
    
def update(object):
    session = Session()
    session.merge(object)
    session.commit()
    session.close()
    
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