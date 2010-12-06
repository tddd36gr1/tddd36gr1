#coding=utf-8
""" EXEMPELKOD för hur man kan använda databasen """

from db import DatabaseWorker
from class_.base_objects import Employee, StatusCode, Mission, TextMessage

db = DatabaseWorker()

db.add_or_update(TextMessage(2, 1, 'Hej!'))
db.add_or_update(StatusCode('Inkommet larm'))
db.add_or_update(StatusCode('Utryckning!'))
db.add_or_update(StatusCode('Slutfort'))
db.add_or_update(Mission('Reparera bro', 15.578, 58.4048, 0.0, 1, "Bro over tannefors ar trasig, du maste fixa den"))
db.add_or_update(Mission('Radda katten i tradet', 15.578, 58.4048, 0.0, 2, "Pricken har fastnat"))
db.add_or_update(Employee('FF:FF:FF:FF:FF' ,'Samuel', 'Svensson'))
db.add_or_update(Employee('FF:FF:FF:FF:F8' ,'Katrin', 'Olsson'))
db.add_or_update(Mission('[hg] brinner', 15.578, 58.4048, 0.0, 3, 'Radda olen'))

test = [(4,1), (4,2), (4,3), (3,2)]
db.insert_missions_to_images(test)
test = [(1,3), (1,4), (2,1), (2,2), (1,2)]
db.insert_missions_to_employees(test)

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


onlineList = []

for employee in db.get_all(Employee):
    if employee.online == True:
        onlineList.append(employee.fname)

for fname in onlineList:        
    print fname


for mission in db.get_all(Mission):
    print mission

for statuscode in db.get_all(StatusCode):
    print statuscode
    
for employee in db.get_all(Employee):
    print employee
    
for textmessage in db.get_all(TextMessage):
    print textmessage
