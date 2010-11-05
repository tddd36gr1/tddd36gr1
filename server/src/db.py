import sqlalchemy
from class_.base_objects import Employee
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine

metadata = MetaData()
engine = create_engine('mysql://pythonserver:tddd36gr1@localhost/pythonserver')
Session = sessionmaker(bind=engine)
session = Session()

def start():
    session.new
    initTables()
    
def initTables():
    employee_table = Table('employee', metadata,
                           Column('idemployee', Integer, primary_key=True),
                           Column('n810mac', String(17)),
                           Column('fname', String(45)),
                           Column('lname', String(45))
    )
    mapper(Employee, employee_table)
    
def add(object):
    session.add(object)
    
def getAll(object):
    return session.query(object).all()

def getOne(object):
    return session.query(object).first()
    
def commit():
    session.commit()