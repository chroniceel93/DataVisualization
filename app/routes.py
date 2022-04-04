# defines all pages that can be reached.

from flask import current_app as app
from flask import render_template, request, session, render_template_string, redirect, url_for
from flask_session import Session
from . import db, login

server_session = Session(app)

@app.route('/')
def index():
	return render_template("template.html.jinja")

@app.route('/linepage')
def linepage():
	return render_template("linepage.html.jinja")

@app.route('/barpage')
def barpage():
	return render_template("barpage.html.jinja")

@app.route('/piepage')
def piepage():
	return render_template("piepage.html.jinja")

@app.route('/donutpage')
def donutpage():
	return render_template("donutpage.html.jinja")

@app.route('/scatterpage')
def scatterpage():
	return render_template("scatterpage.html.jinja")

@app.route('/bubblepage')
def bubblepage():
	return render_template("bubblepage.html.jinja")

@app.route('/radarpage')
def radarpage():
	return render_template("radarpage.html.jinja")

@app.route('/polarpage')
def polarpage():
	return render_template("polarpage.html.jinja")

@app.route('/viewpage')
def viewpage():
	return render_template("viewpage.html.jinja")

@app.route('/importpage')
def importpage():
	return render_template("importpage.html.jinja")

@app.route('/dbtest')
def dbtest_allfields():
    return render_template("dbtest.html.jinja", string="Have fun!")
    
# These do not return actual webpages, just raw JSON data.
@app.route('/db_all')
def db_all():
    access = db.DBData(user='johndoe'
                     , password='password'
                     , host='localhost'
                     , schema='employees'
                     , port='3306')
    return access.get_all()

@app.route('/request', methods=['POST'])
def req():
    query = request.form
    access = db.DBData(user='johndoe'
                    , password='password'
                    , host='localhost'
                    , schema='employees'
                    , port='3306')
    
    return access.request(query.get('type')
                        , query.get('itemA')
                        , query.get('itemB')
                        , query.get('filter')
                        , query.get('step'))

@app.route('/login', methods=['GET', 'POST'])
def login_TEST():
    error = None
    accessdb = db.DBUser()
    login_access = login.Login(access=accessdb)
    if request.method == 'POST':
        uuid = login_access.UserValidate(username=request.form['username'], password=request.form['password'])
        if uuid == None:
            error = 'Username or password was incorrect. Please try again.'
        else:
            return render_template("template.html.jinja")
    return render_template("login.html.jinja", error=error)


@app.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = str(request.form['email_address'])
        return redirect(url_for('get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """


@app.route('/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('set_email') }}">here.</a></h1>
            {% endif %}
        """)


@app.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'

@app.route('/api_test')
def api_test():
    access = db.DBUser()
    return access.get_all()

@app.route('/create_test_user')
def create_test_user():
    accessdb = db.DBUser()
    login_access = login.Login(access=accessdb)
    return login_access.UserAdd(username='JohnDoe', password='password', email='JohnDoe@email.com')
    

@app.route('/validate_test_user')
def validate_test_user():
    accessdb = db.DBUser()
    login_access = login.Login(access=accessdb)
    return login_access.UserValidate(username='JohnDoe', password='password')

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