# coding: utf-8

import psycopg2
import psycopg2.extras

def startdbc():
    conn = psycopg2.connect(
    host = 'localhost',
    database = 'university',
    user = 'rector',
    password = 'rector'
#    user = 'postgres',
#    password = 'postgres'
)
    conn.set_client_encoding('UNICODE')
    return conn;

def stopdbc(db):
    db.commit()
    db.close()

def cursor(db):
    return db.cursor()

def dict_cursor(db):
    return db.cursor(cursor_factory=psycopg2.extras.DictCursor)

def testdbc(db):
    cur=db.cursor()
    cur.execute("SELECT lower('ТЕКСТ') as text, 2+3 as num")
    posts=[dict(id=i[0],title=i[1]) for i in cur.fetchall()]
    print posts[0]['id'],  posts[0]['title']
    print posts[0].values()

def get_specializations(db):
    cur=db.cursor()
    cur.execute("SELECT id, display_name as name from specializations")
#            specializations=[dict(id=i[0],name=i[1]) for i in cur.fetchall()]
#            можно свернуть cur.fetchall().items(), но кодировка...

    specializations=[]
    for i in cur.fetchall():
        specializations.append((i[0],i[1].decode('utf-8')),)
    return specializations

def get_subjects(db):
    cur=db.cursor()
    cur.execute("SELECT id, name FROM subjects")
#            subjects=[dict(id=i[0],name=i[1]) for i in cur.fetchall()]
#            не забыть свернуть
    subjects=[]
    for i in cur.fetchall():
        subjects.append((i[0],i[1].decode('utf-8')),)
    return subjects

if __name__ == "__main__":
    db = startdbc()
    testdbc(db)
    stopdbc(db)

