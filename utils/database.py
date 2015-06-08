# coding: utf-8

import psycopg2
import psycopg2.extras

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

def testdbc(db):
#    cur=db.cursor()
    cur =    db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * from students where id=990")
#    xx = cur.fetchone()
#    d = [dict(zip([column[0] for column in cur.description], row))
#             for row in cur.fetchall()]
#    d = zip ([column[0] for column in cur.description], cur.fetchone())
#    d = zip ([column[0] for column in cur.description], cur.fetchone())
#    d = [],
#    for column in cur.description:
#        print column
    rec = cur.fetchone()
    print rec
#    print d
#    print    d['id']
#    posts=[dict(id=i[0],title=i[1]) for i in cur.fetchall()]
#    print posts[0]['id'],  posts[0]['title']
#    print posts[0].values()


if __name__ == "__main__":
    db = startdbc()
    testdbc(db)
    stopdbc(db)

