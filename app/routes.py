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
def dbtest():
    return render_template("dbtest.html.jinja", string=db.get_test())

@app.route('/dbtest/tables')
def dbtest_tables():
	return render_template("dbtest.html.jinja", string=db.get_table_list())

@app.route('/dbtest/columns')
def dbtest_columns():
    return render_template("dbtest.html.jinja", string=db.get_table_columns("employees"))

@app.route('/dbtest/items')
def dbtest_items():
    return render_template("dbtest.html.jinja", string=db.get_all_data("employees", "first_name"))