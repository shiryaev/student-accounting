# coding: utf-8

import psycopg2
import psycopg2.extras
from psycopg2._psycopg import IntegrityError

from random import shuffle

def startdbc():
    return psycopg2.connect(
    host = 'localhost',
    database = 'university',
    user = 'rector',
    password = 'rector'
#    user = 'postgres',
#    password = 'postgres'
)

def stopdbc(db):
    db.commit()
    db.close()

def get_specializations(db):
    cur=db.cursor()
    cur.execute("SELECT id, display_name as name from specializations")
    specializations=[]
    for i in cur.fetchall():
        specializations.append((i[0],i[1].decode('utf-8')),)
    return specializations

def get_subjects(db):
    cur=db.cursor()
    cur.execute("SELECT id, name FROM subjects")
    subjects=[]
    for i in cur.fetchall():
        subjects.append((i[0],i[1].decode('utf-8')),)
    return subjects


def add_plan(db):
#    cur=db.cursor()
    specializations = get_specializations(db)
    subjects = get_subjects(db)
#    shuffle(subjects)
    for specialization in specializations:
        for c in xrange(1,7):
            for w in [True, False]:
                shuffle(subjects)
                for s in xrange(0,11):
                    cur=db.cursor()
                    id = None;
                    try:
                        cur.callproc("add_plan",[subjects[s][0],specialization[0],c, w,None,None])
                        id=cur.fetchone()[0];
                    except IntegrityError as e:
                        print 'error'



if __name__ == "__main__":
    db = startdbc()
    add_plan(db)
    stopdbc(db)

