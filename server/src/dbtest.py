#coding=utf-8
""" EXEMPELKOD för hur man kan använda databasen """

from db import DatabaseWorker
from class_.base_objects import Employee, StatusCode, Mission, TextMessage

db = DatabaseWorker()

#db.add_or_update(TextMessage('192.168.2.15', '192.168.2.15', 'Brunk'))
#db.add_or_update(StatusCode('Inkommet larm'))
#db.add_or_update(StatusCode('Utryckning!'))
#db.add_or_update(StatusCode('Slutfort'))
#db.add_or_update(Mission('Brunka', 15.578, 58.4048, 0.0, 1, "Bajsa och runka samtidigt"))
#db.add_or_update(Mission('Bajsa', 15.578, 58.4048, 0.0, 2, "Skita"))
#db.add_or_update(Employee('FF:FF:FF:FF:FF' ,'Adolf', 'Hitler'))
#db.add_or_update(Mission('Runka', 15.578, 58.4048, 0.0, 3, 'Ga pa dejt med hogerhanden'))


#for i in range(1, 15):
#    db.add_or_update(Mission('Testa stuff', 15.578, 58.4048, 0.0, 2))
#db.add_or_update(Employee('FF:FF:AS:DF:13:37','Samuel', 'Svensson'))
#db.get_one(Mission).title = "Pwn"

"""
Example for assigning a mission to an employee:
    db.get_one_by_id(Employee, 1).missions.append(db.get_one_by_id(Mission, 3))
"""
for mission in db.get_all(Mission):
    print mission

for statuscode in db.get_all(StatusCode):
    print statuscode
    
for employee in db.get_all(Employee):
    print employee
    
for textmessage in db.get_all(TextMessage):
    print textmessage