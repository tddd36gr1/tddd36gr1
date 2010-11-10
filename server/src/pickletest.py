#coding=utf8

import cPickle as pickle

import db
from class_.base_objects import Employee, StatusCode, Mission

p1 = pickle.dumps(db.get_one(Employee))

olle = pickle.loads(p1)

print olle