# defines all pages that can be reached.

from flask import current_app as app
from flask import render_template
from . import db

@app.route('/')
@app.route('/index')
def index():
	return "Hello, Flask!"

@app.route('/template')
def temp():
	return render_template("template.html")

@app.route('/linepage')
def linepage():
	return render_template("linepage.html")

@app.route('/barpage')
def barpage():
	return render_template("barpage.html")

@app.route('/scatterpage')
def scatterpage():
	return render_template("scatterpage.html")

@app.route('/dbtest')
def dbtest_allfields():
    return render_template("dbtest.html.jinja", string="Cool stuff!")
    #return render_template("dbtest.html.jinja", string=db.get_all())
    
    
# These do not return actual webpages, just raw JSON data.
@app.route('/db_all')
def db_all():
    return db.get_all()

@app.route('/db_result')
def db_result():
    return db.join("salary", "gender", "salaries", "employees")

@app.route('/request')
def req():
    return db.request(0, "salaries,salaries", "salaries,from_date,date", 0)

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