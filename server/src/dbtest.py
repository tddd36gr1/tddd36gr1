import db
from class_.base_objects import *

db.start()

#test_employee = Employee('SA:SA:SS:SA:SA','Flamenco', 'De la Vida')
#db.add(test_employee)
#db.commit()

for employee in db.getAll(Employee):
    print employee

print 'MAC: '+db.getOne(Employee).n810mac