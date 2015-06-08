# coding: utf-8
# можно всё сделать и в базе, но проверим время выполнения

from database import *
from datetime import datetime, timedelta
import random
# распределение оценок
marks = 2,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5
db = startdbc()
fake=db.cursor()
fake.execute("select student_id, plan_id, date  from fmarks")

#INSERT INTO mark(student_id, plan_id, date, value) VALUES (?, ?, ?, ?);

cl = 0
while True:
    row = fake.fetchone()
    if row is None:
        break
    row = list(row)+[random.choice (marks)]
    db.cursor().callproc("add_mark",row);
    cl+=1
    if cl > 10000:
        cl = 0
	print 'committed 10000'
        db.commit()
stopdbc(db);
