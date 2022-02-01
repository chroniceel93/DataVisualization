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

@app.route('/dbtest')
def dbtest():
    return render_template("dbtest.html.jinja", string=db.get_test())
