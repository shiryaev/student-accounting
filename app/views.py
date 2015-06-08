# coding: utf-8
from flask import render_template, request, redirect, abort, url_for, flash
from datetime import date
import json
from psycopg2 import IntegrityError
from app import app
from database import startdbc, stopdbc, get_specializations, dict_cursor, get_subjects
from forms import GroupForm, StudentSearchForm, PlanForm, MarkSearchForm
from math import ceil


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page


class Pagination(object):
    def __init__(self, page, per_page, total_count, search_hash):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.search_hash = search_hash

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def hash(self):
        return self.search_hash

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or num > self.pages - right_edge \
                    or (self.page - left_current - 1 < num < self.page + right_current):
                if last + 1 != num:
                    yield None
                yield num
                last = num


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


@app.route("/")
@app.route("/index/")
def index():
    return render_template('index.html')


@app.route('/group/', methods=['GET', 'POST'])
@app.route('/group/<int:id>')
def group(id=None):
    form = GroupForm()
    db = startdbc()

    if id is not None:
        cur = db.cursor()
        cur.execute("SELECT name, year, specialization_name from groups where id = %s", [id])
        res = cur.fetchone()
        stopdbc(db)
        if res is None:
            # TODO: Сюда лучше flash
            abort(404)
        (name_data, year_data, specialization_data) = res
        # TODO: почему нужно перекодировать?
        # http://stackoverflow.com/questions/5040532/python-ascii-codec-cant-decode-byte
        # https://github.com/psycopg/psycopg2/blob/master/examples/encoding.py
        specialization_data = unicode(specialization_data, "utf8")
        name_data = unicode(name_data, "utf8")
        return render_template('group.html', read=True, id=id, form=form, name_data=name_data, year_data=year_data,
                               specialization_data=specialization_data)

    # получить специализации,
    form.specializationsf.choices = get_specializations(db)

    if form.validate_on_submit():  # в т.ч. request.method == 'POST':
        # добавление новой группы, если успешно, то открыть её просмотр
        cur = db.cursor()
        cur.callproc("add_group", [form.namef.data, form.specializationsf.data, form.yearf.data])
        id = cur.fetchone()[0]
        stopdbc(db)
        # TODO:  почему url_for cant find id?
        # http://127.0.0.1:5000/group/?id=10
        #        return redirect(url_for('group', id=id))
        return redirect(url_for('group') + str(id))  # "{}".format()

    else:
        #  показать форму для создания новой группы
        stopdbc(db)
        return render_template('group.html', title=u"Создание учебной группы", read=False, form=form)


@app.route('/del_group/', methods=['POST'])
def del_group():
    id = request.form['id']
    if id is None:
        flash(u'Не указана группа к удалению!', 'error')
        return redirect(url_for('index'))

    db = startdbc()
    cur = db.cursor()
    cur.execute("SELECT name from groups where id = %s", [id])

    res = cur.fetchone()

    if res is None:
        flash(u'Группа с данным идентификатор не найдена в базе!', 'error')
        stopdbc(db)
        return redirect(url_for('index'))
    cur = db.cursor()
    try:
        cur.callproc('del_group', [id])
    except:
        # нехорошо ловить любой ex
        flash(u'Ошибка удаления группы из базы!', 'error')
    else:
        flash(u'Группа %s удалена, студенты отчислены!' % res[0], 'error')
    finally:
        stopdbc(db)
    return redirect(url_for('index'))


@app.route('/students/', methods=['GET', 'POST'])
def students():
    db = startdbc()

    form = StudentSearchForm()
    specializations = get_specializations(db)
    specializations.insert(0, (0, u'Любая'))
    form.specializationsf.choices = specializations

    search_set = None
    search_result = []
    # TODO: смотреть на search_result pagination
    pagination = None
    if request.method == "POST":
        per_page = form.pages_countf.data
        search_set = form.surnamef.data, form.namef.data, form.groupf.data, form.coursef.data, form.specializationsf.data, per_page
        search_hash = str(hash(search_set))
        page = form.page_number.data if form.search_hash.data == search_hash else 1
        # form.page_number.process_data(search_hash)
        # TODO: можно оптимизировать и не всегда запрашивать общее число студентов по запросу
        # но и база же своё делает, можно тут секунд на 10 хэшировать
        cur = db.cursor()
        search_set = list(search_set[:-1])
        cur.callproc("count_students", search_set)

        count_students = cur.fetchone()[0]
        search_set.append(page)
        search_set.append(per_page)

        cur = db.cursor()
        cur.callproc("get_studentse", search_set)

        search_result = cur.fetchall()
        stopdbc(db)
        if (search_result):
            pagination = Pagination(page, per_page, count_students, search_hash)

    # я поздно узнал, что flask создаёт внутри jinja2 глобальные переменные типа request и не надо лишний раз передавать
    return render_template('student_search.html', form=form, pagination=pagination, search_set=json.dumps(search_set),
                           search_result=search_result)


@app.route('/planing/', methods=['GET', 'POST'])
@app.route('/planing/<int:id>')
def planing(id=None):
    title = u"Создание планов по специальностям"
    error = None
    db = startdbc()

    form = PlanForm()
    form.specializationsf.choices = get_specializations(db)
    form.subjectf.choices = get_subjects(db)
    if request.method == 'POST':
        # TODO: проверить причину coerce=bool, data всегда true, пока на coerce=int
        winter = form.winterf.data == 1
        for subject in form.subjectf.data:
            cur = db.cursor()
            try:
                cur.callproc("add_plan",
                             [subject, form.specializationsf.data, form.coursef.data, winter, form.yearf.data,
                              form.hoursf.data])
                id = cur.fetchone()[0]
            except IntegrityError as e:
                # IntegrityError: duplicate key value violates unique constraint "rule5"
                # TODO: add error message
                # если одну добавляли "Данная дисциплина уже назначена"
                error = u"Ряд дисциплин уже существуют для специальности"
                pass
            db.commit()
        stopdbc(db)
        if id is None and error is None:
            error = u"Неизвестная ошибка"
        if error is not None:
            return render_template('planing.html', title=title, form=form, id=id, error=error)

        # TODO:  почему url_for cant find id?
        # http://127.0.0.1:5000/planing/?id=10
        return redirect(url_for('planing', id=id))
    # return redirect(url_for('planing')+str(id)) # "{}".format()
    else:
        stopdbc(db)
        return render_template('planing.html', title=title, form=form, id=id)


@app.route('/student_card/<int:id>', methods=['GET', 'POST'])
def student_card(id=None):
    if id is None:
        abort(404)
    db = startdbc()
    cur = dict_cursor(db)
    cur.execute("SELECT * from students where id=%s", (id,))
    card = cur.fetchone()
    if card is None:
        stopdbc(db)
        abort(404)
    form = MarkSearchForm()
    from_year = int(card['year'])
    to_year = date.today().year
    years = []
    for year in xrange(to_year, from_year - 1, -1):
        course = year - from_year + 1
        years.append((course, u"{}/{} ({} курс)".format(year, year + 1, course)), )
    form.yearf.choices = years
    year = form.yearf.data if request.method == 'POST' else to_year - from_year + 1
    winter = form.winterf.data == 1 if request.method == 'POST' else True

    cur = db.cursor()
    cur.callproc("get_marks", [id, year, winter])
    # Этот запрос был менее оптимальный
    # cur.execute("""SELECT subject_name, hours, date, value from marks \
    #                where student_id = %s and year = %s and winter = %s \
    #                order by subject_name""", (id, year, winter))
    search_result = cur.fetchall()
    stopdbc(db)
    return render_template('student_card.html', card=card, id=id, form=form, search_result=search_result)
