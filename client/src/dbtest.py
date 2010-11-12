#coding=utf8

""" EXEMPELKOD för hur man kan använda databasen """

import db
from class_.base_objects import Employee, StatusCode, Mission
import requesthandler

#db.add(StatusCode('Done'))
#db.add(Mission('Brunka', 12.2, 13.4, 0.0, 1))
#olle = Employee('00:00:00:00:00', 'Olle', 'Karlsson')
#db.add(olle)

#requesthandler.request((Employee('AA:AA:AA:BB:AA', 'MASDO', 'Svensson')), 'db_add_or_update')
#db.add(StatusCode('Slutfört'))
#db.add(Mission('Se pa film', 0.0, 0.0, 0.0, 2))

#print db.get_one(Employee)
for employee in db.get_all(Employee):
    print employee
    
for mission in db.get_all(Mission):
    print mission
    
for statuscode in db.get_all(StatusCode):
    print statuscode