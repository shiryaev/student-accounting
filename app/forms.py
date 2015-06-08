# coding: utf-8
from flask.ext.wtf import Form

from wtforms import TextField, SelectField, validators, RadioField, IntegerField, SelectMultipleField, HiddenField
from wtforms.validators import Required
from datetime import date

NUM_OF_ACADEMIC_YEARS = 10
COUNT_COURSES = 6


class PlanForm(Form):
    year = date.today().year
    year_choices = [(y, str(y)) for y in xrange(year + 1, year - NUM_OF_ACADEMIC_YEARS, -1)]
    year_choices[0] = (0, u'Любой')
    yearf = SelectField(u'Год действия:', coerce=int, choices=year_choices, default=0)
    specializationsf = SelectField(u'Специальность:', coerce=int, validators=[Required()])
    course_choices = [(y, str(y)) for y in xrange(1, COUNT_COURSES + 1)]
    coursef = SelectField(u'Курс:', coerce=int, choices=course_choices, default=year)
    #    winterf = RadioField(u'Сессия:', coerce=bool, choices= [(True,u'Зимняя'),(False,u'Летняя')], default=True)
    winterf = RadioField(u'Тип сессии:', coerce=int, choices=[(1, u'Зимняя'), (0, u'Летняя')], default=1)
    # subjectf = SelectField(u'Дисциплина:', coerce=int, validators = [Required()])
    subjectf = SelectMultipleField(u'Дисциплины:', coerce=int, validators=[Required()])
    hoursf = IntegerField(u'Нагрузка:')


# hoursf = IntegerField(u'Нагрузка:', [validators.NumberRange(min=2000, max=year+1)])

class GroupForm(Form):
    year = date.today().year
    yearf = SelectField(u'Год поступления:', coerce=int,
                        choices=[(y, str(y)) for y in xrange(year, year - NUM_OF_ACADEMIC_YEARS, -1)], default=year)
    specializationsf = SelectField(u'Специальность:', coerce=int, validators=[Required()])
    namef = TextField(u'Название группы:', [validators.required(), validators.length(max=255)])


class MarkSearchForm(Form):
    year = date.today().year
    winterf = SelectField(u'Тип сессии:', coerce=int, choices=[(1, u'Зимняя'), (0, u'Летняя')], default=1)
    yearf = SelectField(u'Учебный год:', coerce=int, default=year)
    page_scroll_x = TextField(u'прокрутка страницы по оси Х', default='0')
    page_scroll_y = TextField(u'прокрутка страницы по оси Y', default='0')


class StudentSearchForm(Form):
    namef = TextField(u'Имя:', [validators.length(max=100)])
    surnamef = TextField(u'Фамилия:', [validators.length(max=100)])
    specializationsf = SelectField(u'Специальность:', coerce=int, default=0)
    course_choices = [(y, str(y)) for y in xrange(0, COUNT_COURSES + 1)]
    course_choices[0] = (0, u'Любой')
    coursef = SelectField(u'Курс:', coerce=int, choices=course_choices, default=0)
    groupf = TextField(u'Группа:', [validators.length(max=10)])
    # HiddenField невыгодно, т.к. для него нельзя выставить coerce=int
    page_number = IntegerField(u'Номер страницы в поиске', default=1)
    search_hash = TextField(u'Хэш предыдущего поиска')

    pages_countf = SelectField(u'Записей на страницу:', coerce=int,
                               choices=[(5, '5'), (10, '10'), (20, '20'), (30, '30'), (50, '50')], default=10)
