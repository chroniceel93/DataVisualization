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
    return render_template("dbtest.html.jinja", string="Cool stuff!")
    #return render_template("dbtest.html.jinja", string=db.get_all())
    
    
# These do not return actual webpages, just raw JSON data.
@app.route('/db_all')
def db_all():
    return db.DB.get_all()

@app.route('/request')
def req():
    """ This function returns the JSON formatted results of an abstracted SQL request.
    
    The abstraction currently relies on a few core assumptions. We will only be returning two fields per request, and we will only average or sum the requests. The current syntax is designed so that it can be extended.
    
    The structure is as follows: TYPE, ITEMX, ITEMY, STEP
    
    TYPE is an enum that determines what operation is performed on the selected data. Currently, we will only support SUM and AVG.
    
    ITEMX is the data we wish to view, and it is given as a CSV string containing either two ("Table,Item") or three ("Table,Item,Value") items. In order, these define the table the item exists in, the item's field, and if supplied, what value we are looking for.
    
    ITEMY is our scale, given as a CSV string, containing exactly three items ("Table,Item,Type"). The rationale here is slightly different, as since we are using this entry to determine scale, the relevant SQL syntax is type dependent. We will not be searching for a given Value here.
    
    Finally, STEP. This value is used to change the granularity of the input. With very large databases, it might be expected that several hundred thousand results may come back for a given query, leading to a response in the order of hundreds of megabytes. This puts an undue strain on the web-server, the network and the web application for little or no gain. So, increasing the STEP size will decrease the granularity of the data.
    
    #TODO: DATE specific STEP settings.
    #TODO: Implement STEPs, for that matter. Based on resultion/result size?
    #TODO: Define ENUM

    Returns:
        string: JSON String containing result of abstracted SQL query
    """
    return db.DB.request(0, "salaries,salary", "salaries,from_date,date", 0)

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