#coding=utf8
import push
from db import DatabaseWorker

db = DatabaseWorker()
push.pushStart(db)