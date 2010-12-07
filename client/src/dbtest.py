#coding=utf-8
""" EXEMPELKOD för hur man kan använda databasen """

from db import DatabaseWorker
from class_.base_objects import *
import SETTINGS

db = DatabaseWorker()

#db.add_or_update(StatusCode('Inkommet larm'))
#db.add_or_update(StatusCode('Utryckning!'))
#db.add_or_update(StatusCode('Slutfort'))
#db.add_or_update(Mission('Brunka', 34.578, 60.4048, 0.0, 1))
#db.add_or_update(Mission('Bajsa', 15.278, 58.5048, 0.0, 2, 'A cinderella story'))
#db.add_or_update(Mission('StorBrunk', 15.568, 58.4058, 0.0, 3, 'Du ska kora tills det svartnar'))
#db.add_or_update(Mission('Klippa Wibbe', 15.562, 58.4052, 0.0, 1, 'Cutta han!'))
#db.add_or_update(Employee("FF:EE:FF:EE:FF:EE", "Johan", "Aberg"))
#db.add_or_update(Employee('FF:FF:FF:FF:FF' ,'Samuel', 'Svensson'))
#db.add_or_update(Mission('Brunka', 34.578, 60.4048, 0.0, 1, "Runka, fast battre"))
#db.add_or_update(Mission('Bajsa', 15.278, 58.5048, 0.0, 2, 'A cinderella story'))
#db.add_or_update(Mission('StorBrunk', 15.568, 58.4058, 0.0, 3, 'Du ska kora tills det svartnar'))
#db.add_or_update(Mission('Klippa Wibbe', 15.562, 58.4052, 0.0, 1, 'Cutta han!'))
#db.get_one(Employee).missions.append(db.get_one(Mission))
#db.get_one_by_id(Employee, SETTINGS.employee_id).missions.append(db.get_one(Mission))
#db.commit()
#for i in range(1, 10):
#    db.add_or_update(Mission('Radda katten i tradet', 15.578, 58.4048, 0.0, 2))
#db.add_or_update(Employee('FF:FF:AS:DF:13:37','Samuel', 'Svensson'))
#db.get_one(Mission).title = "Pwn"
#db.add(TextMessage(2, 1, "Sieg!"))
#img = MissionImage("Mitt huvud", "xray.jpg")
#db.add(img)
#db.get_one(Mission).images.append(img)
#db.commit()

#for mission in db.get_all(Mission):
#    list.append((mission.lat, mission.long))
"""
for mission in db.get_all(Mission):
    print mission.employees

for statuscode in db.get_all(StatusCode):
    print statuscode
"""    
for employee in db.get_all(Employee):
    print employee

for image in db.get_all(MissionImage):
    print image