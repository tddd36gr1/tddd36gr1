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

#for i in range(1, 15):
#    db.add_or_update(Mission('Testa stuff', 15.578, 58.4048, 0.0, 2))
#db.add_or_update(Employee('FF:FF:AS:DF:13:37','Samuel', 'Svensson'))
#db.get_one(Mission).title = "Pwn"

"""
Example for assigning a mission to an employee:
    db.get_one_by_id(Employee, 1).missions.append(db.get_one_by_id(Mission, 3))
"""
#gnag = db.get_one_by_id(Employee, 2)
#gnag.online = True
#db.commit()


#onlineList = []
#
#for employee in db.get_all(Employee):
#    if employee.online == True:
#        onlineList.append(employee.fname)
#
#for fname in onlineList:    
#        
#    print fname
#
#
#for mission in db.get_all(Mission):
#    print mission.images
#
#for statuscode in db.get_all(StatusCode):
#    print statuscode
#    
#for employee in db.get_all(Employee):
#    print employee
#    
#for textmessage in db.get_all(TextMessage):
#    print textmessage
#
#for missionimage in db.get_all(MissionImage):
#    print missionimage

#placemark = Placemark("snoppen suger", 15.5, 78.8, "Sug min hestarfifan", 1)
#db.add_or_update(placemark)