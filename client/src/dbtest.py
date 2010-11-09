# coding=utf8

""" EXEMPELKOD för hur man kan använda databasen """

import db
from class_.base_objects import Employee, StatusCode, Mission

#db.add(StatusCode('Done'))
#db.add(Mission('Brunka', 12.2, 13.4, 0.0, 1))
olle = Employee('00:00:00:00:00', 'Olle', 'Karlsson')
db.add(olle)

db.add(Employee('AA:AA:AA:AA:AA', 'MONGO', 'Svensson'))
#db.add(StatusCode('Testing'))
#db.add(Mission('Se pa film', 0.0, 0.0, 0.0, 2))

for employee in db.get_all(Employee):
    print employee