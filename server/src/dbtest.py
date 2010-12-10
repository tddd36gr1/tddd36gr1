#coding=utf-8
""" EXEMPELKOD för hur man kan använda databasen """

import db
from class_.base_objects import *

db = db.database

#db.add_or_update(TextMessage(2, 1, 'Hej!'))
#db.add_or_update(StatusCode('Inkommet larm'))
#db.add_or_update(StatusCode('Utryckning!'))
#db.add_or_update(StatusCode('Slutfort'))
#db.add_or_update(Mission('Reparera bro', 15.578, 58.4048, 0.0, 1, "Bro over tannefors ar trasig, du maste fixa den"))
#db.add_or_update(Mission('Radda katten i tradet', 15.578, 58.4048, 0.0, 2, "Pricken har fastnat"))
#db.add_or_update(Employee('CF:FF:FF:FF:FF' ,'Samuel', 'Svensson'))
#db.add_or_update(Employee('DF:FF:FF:FF:F8' ,'Katrin', 'Olsson'))
#db.add_or_update(Mission('[hg] brinner', 15.578, 58.4048, 0.0, 3, 'Radda olen'))
#db.add_or_update(MissionText("Hej", 2))
#db.add_or_update(MissionImage("Yo", "Heaasasddasdjs.jpg"))

"""
Example for assigning a mission to an employee:
    db.get_one_by_id(Employee, 1).missions.append(db.get_one_by_id(Mission, 3))
"""

for mission in db.get_all(Mission):
    print mission.images

for statuscode in db.get_all(StatusCode):
    print statuscode
    
for employee in db.get_all(Employee):
    print employee
    
for textmessage in db.get_all(TextMessage):
    print textmessage
    
for missiontext in db.get_all(MissionText):
    print missiontext

for missionimage in db.get_all(MissionImage):
    print missionimage
    
for placemark in db.get_all(Placemark):
    print placemark