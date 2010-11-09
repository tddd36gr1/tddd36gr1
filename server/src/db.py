# coding=utf8

from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine
from class_ import base_objects

#Initializing database by opening MySQL-database
#and creating a new Sfrom sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import relation, backref

#Declarative base for automatic mapping of objects to database tables
Base = declarative_base()

class Employee(Base):
    """
    An employee-object, each employee has one n810-tablet assigned to him/her, defined by its MAC-address
    """
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    #MAC-address
    n810mac = Column(String(17), unique=True)
    fname = Column(String(45))
    lname = Column(String(45))

    def __init__(self, n810mac, fname, lname):
        """Constructor setting variables"""
        self.fname = fname
        self.lname = lname
        self.n810mac = n810mac
        
    def __repr__(self):
        """String-representation of object in xml"""
        s = "<Employee>"
        s += "\n\t<n810mac>%s</n810mac>" % (self.n810mac)
        s += "\n\t<fname>%s</fname>" % (self.fname)
        s += "\n\t<lname>%s</lname>" % (self.lname)
        s += "\n</Employee>"
        return s        
    
class StatusCode(Base):
    """StatusCode object, just an id and a name"""
    __tablename__ = 'statuscodes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(45))

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        """String-representation of object in xml"""
        return "<StatusCode>\n\t<name>%s</name>\n</StatusCode>" % self.name
   
class Mission(Base):
    """Mission object, with a lot of placemark-related attributes, like longitude and latitude"""
    __tablename__ = 'missions'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(45))
    long = Column(Float)
    lat = Column(Float)
    rad = Column(Float)
    #Timestamp attribute, haven't found out autotimestamping yet
    timestamp = Column(TIMESTAMP)
    status = Column(Integer, ForeignKey('statuscodes.id'))
    
    #status_name is really a StatusCode object, for getting just the name-string and not 
    #the objects xml-representation, print status_name.name
    status_name = relation(StatusCode, backref=backref('missions', order_by=id))

    def __init__(self, title, long, lat, rad, status):
        """Constructor setting variables"""
        self.title = title
        self.long = long
        self.lat = lat
        self.rad = rad
        self.status = status
        
    def __repr__(self):
        """String-representation of object in xml"""
        s = "<Mission>"
        s += "\n\t<title>%s</title>" % (self.title)
        s += "\n\t<long>%s</long>" % (self.long)
        s += "\n\t<lat>%s</lat>" % (self.lat)
        s += "\n\t<rad>%s</rad>" % (self.rad)
        s += "\n\t<status>%s</status>" % (self.status)
        s += "\n</Mission>"
        return s

def create_tables(engine):
    """Function for creating all database-tables"""
    Base.metadata.create_all(engine)QLAlchemy session
engine = create_engine('mysql://pythonserver:tddd36gr1@localhost/pythonserver')
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