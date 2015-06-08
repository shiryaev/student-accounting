# coding: utf-8
import csv
from database import *
from datetime import datetime, timedelta
import random

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

# минимальное и максимально количество студентов в группе
min_students_in_group = 20
max_students_in_group = 25

# cредний возрасто первокурсника
freshman_age=17


#закончили на группе 73407 : Крысанова Людмила Геннадьевна
#Шмальнул 8000 студентов, добавил(!) их к skip, занулил count для защиты от запуска
count = 0
skip = 8000

groups_file = 'groups.txt'
names = 'fio20000.txt'

group_names = []
for line in  open(groups_file).readlines():
    group_names+=[line.rstrip('\n')]*random.randint(min_students_in_group, max_students_in_group)

with open(names) as csvfile:
#    reader = unicode_csv_reader(csvfile)
    reader = csv.reader(csvfile, delimiter=' ')
    db = startdbc()
    groups = {}
    future_year = date.today().year;
    st = 0;
    for row in reader:
        if st < skip:
            st+=1
            continue
        if st >= count+skip:
            break
        surname = row[0].decode('utf-8')
        patronymic = row[2].decode('utf-8')
        name = row[1].decode('utf-8')
        gname = group_names[st]
        st+=1
        fio = ' '.join([surname, name, patronymic])
        gid = groups[gname] if gname in groups else None
        if gid is None:
#            gid = 0
#        elif False:
#         пробуем извлечь по номеру группы 
            cur=db.cursor()
            cur.execute("select id from groups where name = %s",(gname,))
            grow = cur.fetchone()
            if grow is None:
                cur=db.cursor()
                print "add group %s" % gname
                cur.callproc("add_group",[gname]);
                grow=cur.fetchone();
            gid = grow[0];
        if gid is None:
            print u'не смог добавить группу %s для %s', gname, fio;
            break;
        else:
            groups[gname] = gid;
        # самопалка: определение пола по ФИО
        g = 'M' if (patronymic[-2:] == u'ич' or surname[-2:] == u'ов')  else ('F' if patronymic[-2:] == u'на' or name[-1] in  (u'а', u'я') or surname[-1] == u'а' else ('M' if name[-2:] == u'ан' else None))
        year=future_year-freshman_age-int(gname[2])
        year = random.randint(year-1, year+1)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        # чтобы убрать косяки с отсутствием 29-31 чисел чутка двигаем дату на random
        birth_date = datetime(year, month, day) + timedelta(days=random.randint(1, 5))
        birth_date =psycopg2.Date(birth_date.year,birth_date.month,birth_date.day)
        student = [surname,name,patronymic,g,birth_date,gid]
#        print student
#        continue
        cur=db.cursor()        
        cur.callproc("add_student",student);
        srow=cur.fetchone();
        if srow is None:
            print u"не смог добавить студента", fio
        else:
            print fio, str(srow[0])
        db.commit()
    stopdbc(db);
 

