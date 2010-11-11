#coding=utf8

""" EXEMPELKOD för hur man kan använda databasen """

import db
from class_.base_objects import Employee, StatusCode, Mission
import networkcomponent

#db.add(StatusCode('Done'))
#db.add(Mission('Brunka', 12.2, 13.4, 0.0, 1))
olle = Employee('00:00:00:00:00', 'Olle', 'Karlsson')

networkcomponent.send('127.0.0.1',olle,'data')
