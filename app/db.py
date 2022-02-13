from flask import current_app, g
import mysql.connector
import json
from mysqlx import Row

def connect():
    return mysql.connector.connect( user='johndoe'
                                     , password='password'
                                     , host='localhost'
                                     , database='employees')

# def get_test():
#     # TODO: Pull connection into a utility Class to reduce repeat code, especially w/ tests
#     # NOTE: Test class, serves no real function
#     connection = connect()
#     cur = connection.cursor()
#     cur.execute("SELECT * FROM employees ORDER BY first_name")
#     string = ""
#     for row in cur:
#         string += str(row[2]) + " " + str(row[3]) + " " + str(row[5]) + '<p>'
#     cur.close()
#     connection.close()
#    return string

def get_table_list():
    command = "SHOW TABLES"
    items = execute_com(command)
    return items

def get_table_columns(table):
    command = "SHOW COLUMNS FROM " + table
    items = execute_com(command)
    return items

#NOTE: join is good for debug output, but not useful for actually working w/ data
# we can build dropdowns from raw entries...

def get_all():
    items = get_table_list()
    cols = 0
    result = []
    for x  in range(0, len(items)):
        # string is padded, cut off the first three and last two chars
        cols = get_table_columns(str(items[x])[2:-3])
        for y in range(0, len(cols)):
            # append 2d array element with table name, item name and item type, in that order
            result.append([str(items[x])[2:-3], str(cols[y][0]), str(cols[y][1])[2:-1]])
    return json.dumps(result)
    
def get_all_data(table, item):   
    command = "SELECT " + item + " FROM " + table
    items = execute_com(command)
    return json.dumps(items)

def execute_com(string):
    #TODO: Implement error handling for mysql connection.
    
    connection = mysql.connector.connect( user='johndoe'
                                        , password='password'
                                        , host='localhost'
                                        , database='employees')
    cur = connection.cursor()
    cur.execute(string)
    
    items = cur.fetchall()
    
    cur.close()
    connection.close()
            
    return items