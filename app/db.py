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

def join(itemA, itemB, tableA, tableB):
    command1 = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = \"employees\" AND REFERENCED_TABLE_NAME = \"" + tableA + "\""
    command2 = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = \"employees\" AND REFERENCED_TABLE_NAME = \"" + tableB + "\""
    keyA = execute_com(command1)
    keyB = execute_com(command2)
    for x in range(0, len(keyA)):
        if keyA[x][0] == tableB:
            keyA = keyA[x][1]
            break
            
    for y in range(0, len(keyB)):
        print(y)
        if keyB[y][0] == tableA:
            keyB = keyB[y][1]
            break
    
    # if keyA returned empty
    if (keyA == []):
        #then we use keyB
        command = "SELECT " + itemA + ", " + itemB + \
        " FROM " + tableB + " JOIN " + tableA + \
        " ON " + tableB + "." + keyB + " = " + tableA + "." + keyB
    else:
        #otherwise, we use keyA
        command = "SELECT '" + itemA + "', '" + itemB + \
        "' FROM " + tableB + "JOIN" + tableA + \
        " ON " + tableA + "." + keyA + " = " + tableB + "." + keyA
        
    result = execute_com(command)
    return result

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