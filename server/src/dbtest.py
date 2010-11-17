#coding=utf-8
""" EXEMPELKOD för hur man kan använda databasen """

from db import DatabaseWorker
from class_.base_objects import Employee, StatusCode, Mission

db = DatabaseWorker()

#db.add_or_update(StatusCode('Inkommet larm'))
#db.add_or_update(StatusCode('Utryckning!'))
#db.add_or_update(StatusCode('Slutfort'))
#db.add_or_update(Mission('Radda katten i tradet', 15.578, 58.4048, 0.0, 2))
#db.add_or_update(Employee('FF:FF:AS:DF:13:37','Samuel', 'Svensson'))
#db.get_one(Mission).title = "Pwn"


for mission in db.get_all(Mission):
    print mission

for statuscode in db.get_all(StatusCode):
    print statuscode
    
for employee in db.get_all(Employee):
    print employee