from flask import current_app, g
import mysql.connector

def get_test():
    # TODO: Pull connection into a utility Class to reduce repeat code, especially w/ tests
    connection = mysql.connector.connect(  user='johndoe'
                                     , password='password'
                                     , host='localhost'
                                     , database='employees')
    cur = connection.cursor()
    
    cur.execute("SELECT * FROM employees ORDER BY first_name")
    string = ""
    for row in cur:
        string += str(row[2]) + " " + str(row[3]) + " " + str(row[5]) + '<p>'
    cur.close()
    connection.close()
    return string

def get_table_list(database):
    return

def get_table_items(database, table):
    return

def get_item_fields(database, table, item):
    return
    
def get_all_data(database, table, item, field):
    return