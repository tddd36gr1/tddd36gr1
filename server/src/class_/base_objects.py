#coding=utf8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP, Table, Text
from sqlalchemy.orm import relation, backref

#Declarative base for automatic mapping of objects to database tables
Base = declarative_base()
"""
Skapar en tabell som binder samman mission-ID med ett text-ID
"""
missions_to_texts = Table('missions_to_texts', Base.metadata,
                    Column('missions_id', Integer, ForeignKey('missions.id')),
                    Column('missiontexts_id', Integer, ForeignKey('missiontexts.id')))

class Employee(Base, object):
    """
    An employee-object, each employee has one n810-tablet assigned to him/her, defined by its MAC-address
    """
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    #MAC-address
    n810mac = Column(String(17), unique=True)
    fname = Column(String(45))
    lname = Column(String(45))
    online = Column(Boolean())
    ip = Column(String(20))

    def __init__(self, n810mac, fname, lname):
        """Constructor setting variables"""
        self.fname = fname
        self.lname = lname
        self.n810mac = n810mac
        
    def __repr__(self):
        """String-representation of object in xml"""
        s = "<Employee>"
        s += "\n\t<id>%s</id>" % (self.id)
        s += "\n\t<n810mac>%s</n810mac>" % (self.n810mac)
        s += "\n\t<fname>%s</fname>" % (self.fname)
        s += "\n\t<lname>%s</lname>" % (self.lname)
        s += "\n</Employee>"
        return s      
    
class TextMessage(Base, object):
    """
    A text message
    """
    __tablename__ = 'text_message'
    
    id = Column(Integer, primary_key=True)
    src = Column(String(20))
    dst = Column(String(20))
    msg = Column(String(1024))
    

    def __init__(self, src, dst, msg):
        """Constructor setting variables"""
        self.src = src
        self.dst = dst
        self.msg = msg
        
    def __repr__(self):
        """String-representation of object in xml"""
        s = "<TextMessage>"
        s += "\n\t<id>%s</id>" % (self.id)
        s += "\n\t<source>%s</source>" % (self.src)
        s += "\n\t<destination>%s</destination>" % (self.dst)
        s += "\n\t<message>%s</message>" % (self.msg)
        s += "\n</TextMessage>"
        return s          
    

class StatusCode(Base, object):
    """StatusCode object, just an id and a name"""
    __tablename__ = 'statuscodes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(45))

    def __init__(self, name):
    
        self.name = name
        
    def __repr__(self):
        """String-representation of object in xml"""
        return "<StatusCode>\n\t<id>%s</id>\n\t<name>%s</name>\n</StatusCode>" % (self.id, self.name)
   
class Mission(Base, object):
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
    
    #status_name is really a StatusCode object. For getting just the name-string and not 
    #the objects xml-representation, print status_name.name
    status_object = relation(StatusCode, backref=backref('missions', order_by=id))

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
        s += "\n\t<id>%s</id>" % (self.id)
        s += "\n\t<title>%s</title>" % (self.title)
        s += "\n\t<long>%s</long>" % (self.long)
        s += "\n\t<lat>%s</lat>" % (self.lat)
        s += "\n\t<rad>%s</rad>" % (self.rad)
        s += "\n\t<status>%s</status>" % (self.status)
        s += "\n</Mission>"
        return s
"""
En klass for att lagra missionbeskrivningar
""" 
class MissionText(Base, object):
    __tablename__ = 'missiontexts'
    
    id = Column(Integer, primary_key=True)
    descr = Column(Text)
    
    def __init__(self, text):
        self.descr = text
        #self.missions = relation('Mission', secondary=missions_to_texts, backref=backref('missiontexts', order_by=id))
        
    def __repr__(self):
        return '%r' % self.descr

def create_tables(engine):
    """Function for creating all database-tables"""
    Base.metadata.create_all(engine)