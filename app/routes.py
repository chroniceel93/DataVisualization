# defines all pages that can be reached.

from flask import current_app as app
from flask import render_template, request, session, render_template_string, redirect, url_for
from flask_session import Session
from . import db, login

server_session = Session(app)

@app.route('/')
def index():
    if session.get("UUID") != None:
        return render_template("template.html.jinja")
    else:
        return redirect(url_for('login_page'))
 
@app.route('/template')
def templatepage():
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
    access = db.DBData(
        db_user=session["db_username"],
        db_password=session["db_password"],
        schema=session["schema"],
        ssh_user=session["db_username"],
        ssh_password=session["db_password"],
        host=session["ip"],
        port=session["port"]
    )
    return access.get_all()

@app.route('/request', methods=['POST'])
def req():
    query = request.form
    access = db.DBData(
        db_user=session["db_username"],
        db_password=session["db_password"],
        schema=session["schema"],
        ssh_user=session["db_username"],
        ssh_password=session["db_password"],
        host=session["ip"],
        port=session["port"]
    )
    
    return access.request(type=query.get('type')
                        , itemA=query.get('itemA')
                        , itemB=query.get('itemB')
                        , Filter=query.get('filter')
                        , step=query.get('step'))
    
@app.route('/set_db', methods=['POST'])
def set_db():
    query = request.form
    session['schema'] = str(query.get('schema'))
    session['ip'] = str(query.get('ip'))
    session['port'] = str(query.get('port'))
    session['server_username'] = str(query.get('server_username'))
    session['server_password'] = str(query.get('server_password'))
    session['db_username'] = str(query.get('db_username'))
    session['db_password'] = str(query.get('db_password'))
    return "OK"
    

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    accessdb = db.DBUser()
    login_access = login.Login(access=accessdb)
    if request.method == 'POST':
        uuid = login_access.UserValidate(username=request.form['username'], password=request.form['password'])
        if uuid == None:
            error = 'Username or password was incorrect. Please try again.'
        else:
            session['UUID'] = uuid
            return render_template("template.html.jinja")
    return render_template("login.html.jinja", error=error)

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login_page'))

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
    accessdb = db.DBData(
        db_user=session["db_username"],
        db_password=session["db_password"],
        schema=session["schema"],
        ssh_user=session["db_username"],
        ssh_password=session["db_password"],
        host=session["ip"],
        port=session["port"]
    )
    result = accessdb.get_all()

    return result

# @app.route('/set_db', methods=['POST'])
# def set_db():
#     session['url_db'] == str(request.form["url"])
#     session['port_db'] == str(request.form["port"])
#     session['user_db'] == str(request.form["user"])
    
    

@app.route('/create_test_user', methods=['POST'])
def create_test_user():
    query = request.form
    username = query.get('username')
    password = query.get('password')
    email = query.get('email')
    accessdb = db.DBUser()
    login_access = login.Login(access=accessdb)
    return login_access.UserAdd(
        username=username, 
        password=password, 
        email=email)
    

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