from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)


# cursor is define per app instance, used for DB connection
# there is no *persistent* db connection...

# I'm defining a test-user here, so we can get things up and
# running, but we should really set this up per-instance

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'johndoe'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'employees'

mysql = MySQL(app)

from app import routes

# with app.app_context():
#  cursor = mysql.connection.cursor()
#  cursor.excute("SQL STATEMENT")

# Statement is executed and data is returned

# to print raw result
#  result = cursor.fetchall()
#  cursor.close() 
#  print(result)

