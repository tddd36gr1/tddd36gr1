#coding=utf8

""" EXEMPELKOD för hur man kan använda databasen """

import db
from class_.base_objects import Employee, StatusCode, Mission

#db.add(StatusCode('Done'))
#db.add(Mission('Brunka', 12.2, 13.4, 0.0, 1))
#olle = Employee('00:00:00:00:00', 'Olle', 'Karlsson')
#db.add(olle) 

#db.add(Employee('AA:AA:AA:AA:AA', 'MONGO', 'Svensson'))
#db.add(StatusCode('Testing'))
#db.add(StatusCode('Inkommet larm'))
#db.add(StatusCode('Utryckning!'))
#db.add(Mission('Rädda katten i trädet', 15.578, 58.4048, 0.0, 2))

print db.get_one(Mission).title
#for mission in db.get_all(Mission):
#    print mission