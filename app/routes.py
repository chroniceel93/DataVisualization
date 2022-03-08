# defines all pages that can be reached.

from flask import current_app as app
from flask import render_template
from flask import request
from . import db

@app.route('/')
def index():
	return render_template("template.html.jinja")

@app.route('/linepage')
def linepage():
	return render_template("linepage.html.jinja")

@app.route('/barpage')
def barpage():
	return render_template("barpage.html.jinja")

@app.route('/scatterpage')
def scatterpage():
	return render_template("scatterpage.html.jinja")

@app.route('/dbtest')
def dbtest_allfields():
    return render_template("dbtest.html.jinja", string="Have fun!")
    
# These do not return actual webpages, just raw JSON data.
@app.route('/db_all')
def db_all():
    return db.DB.get_all()

@app.route('/request', methods=['POST'])
def req():
    query = request.form
    return db.DB.request(query.get('type')
                        , query.get('itemA')
                        , query.get('itemB')
                        , query.get('filter')
                        , query.get('step'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'employees' or request.form['password'] != 'employees':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template("template.html.jinja")
    return render_template("login.html.jinja", error=error)


#db.DB.request(0, "salaries,salary", "salaries,from_date,date", 1)

# @app.route('/dbtest')
# def dbtest():
#     return render_template("dbtest.html.jinja", string="<h3> Jnjia & AJAX playground.</h3>")

# @app.route('/dbtest/tables')
# def dbtest_tables():
# 	return render_template("dbtest.html.jinja", string=db.get_table_list())

# @app.route('/dbtest/columns')
# def dbtest_columns():
#     return render_template("dbtest.html.jinja", string=db.get_table_columns("employees"))

# @app.route('/dbtest/items')
# def dbtest_items():
#     return render_template("dbtest.html.jinja", string=db.get_all_data("employees", "first_name, last_name"))

# @app.route('/test')
# def test():
#     db.join("salary", "first_name", "salaries", "employees")
#     return