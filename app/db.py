# Functions for interacting with the database.
# TODO: Put this in a class without breaking it

from logging import addLevelName
from flask import current_app, g, jsonify
import mysql.connector
import json
import csv
from mysqlx import Row

class DB:
    def __connect():
        return mysql.connector.connect( user='johndoe'
                                        , password='password'
                                        , host='localhost'
                                        , database='employees')
        
    def __join(tableA, tableB):
        """ This function generates a snippet of SQL that joins two tables.

        It's fairly naive, first querying for all keys between the two tables,
        and then picking the first matching key pair.

        Args:
            tableA (string): ident for table holding first item
            tableB (string): ident for table holding second item

        Returns:
            string: SQL snippet
        """
        
        # Query database for all keys.
        # FIXME: Schema is currently hardcoded.
        command1 = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = \"employees\" AND REFERENCED_TABLE_NAME = \"" + tableA + "\" "
        command2 = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = \"employees\" AND REFERENCED_TABLE_NAME = \"" + tableB + "\" "
        keyA = DB.__execute_com(command1)
        keyB = DB.__execute_com(command2)
        
        # Check table B for key A.
        for x in range(0, len(keyA)):
            if keyA[x][0] == tableB:
                # If we find it, set KeyA
                keyA = keyA[x][1]
                break
                
        # Check table A for key B
        for y in range(0, len(keyB)):
            print(y)
            if keyB[y][0] == tableA:
                keyB = keyB[y][1]
                break
        
        # if keyA returned empty
        if (keyA == []):
            #then we use keyB
            command = tableA + " JOIN " +  \
            " ON " + tableB + "." + keyB + " = " + tableA + "." + keyB
        else:
            #otherwise, we use keyA
            command =  tableA +" JOIN " + \
            " ON " + tableA + "." + keyA + " = " + tableB + "." + keyA
            
        return command

    def __execute_com(string):
        """ Takes a given string, assuming it is a valid SQL Query, and executes it.

        Args:
            string (string): SQL Query

        Returns:
            type: description (it's complicated, I'll sort it out this weekend?)
        """
        #TODO: Fill out return fields in docstring
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

        
        
    def get_table_list():
        """ Gets a list of all tables in the schema.
        
        NOTE: I don't think this is used.

        Returns:
            string: JSON list of all tables in the schema
        """
        command = "SHOW TABLES"
        items = DB.__execute_com(command)
        return json.dumps(items)

    def get_table_columns(table):
        """Gets a list of all columns in a table.

        Args:
            table (string): A table in the current schema.

        Returns:
            string : JSON list of all columns in the table.
        """
        command = "SHOW COLUMNS FROM " + table
        items = DB.__execute_com(command)
        return json.dumps(items)

    def get_all():
        """ Queries the database for all fields.

        Returns:
            string: A JSON String containing {"table_name", "item_name", "item_type"}
        """
        items = DB.get_table_list()
        cols = 0
        result = []
        for x  in range(0, len(items)):
            # string is padded, cut off the first three and last two chars
            cols = DB.get_table_columns(str(items[x])[2:-3])
            for y in range(0, len(cols)):
                # append 2d array element with table name, item name and item type, in that order
                result.append([str(items[x])[2:-3], str(cols[y][0]), str(cols[y][1])[2:-1]])
        return json.dumps(result)

    def request(type, itemA, itemB, step):
        """ This function returns the JSON formatted results of an abstracted SQL request.

        The abstraction currently relies on a few core assumptions. We will only be returning two fields per request, and we will only average or sum the requests. The current syntax is designed so that it can be extended.
        
        The structure is as follows: TYPE, ITEMA, ITEMB, STEP
        
        TYPE is an enum that determines what operation is performed on the selected data. Pass -1 for no operation (this disables STEP), 0 for AVG, and 1 for SUM.
        
        ITEMA is the data we wish to view, and it is given as a CSV string containing either two ("Table,Item") or three ("Table,Item,Value") items. In order, these define the table the item exists in, the item's field, and if supplied, what value we are looking for.
        
        ITEMB is our scale/y-axis, given as a CSV string. It should contain exactly three items ("Table,Item,Type"). The rationale here is slightly different, as since we are using this entry to determine scale, the relevant SQL syntax is type dependent. We will not be searching for a given value here.
        
        Finally, STEP. This value is used to change the granularity of the input. With very large databases, it might be expected that several hundred thousand results may come back for a given query, leading to a response in the order of hundreds of megabytes. This puts an undue strain on the web-server, the network and the web application for little or no gain. So, increasing the STEP size will decrease the granularity of the data.

        Args:
            type (int): Operation type, (-1=NOP, 0=AVG, 1=SUM)
            itemA (string): Y-axis string, ("Table,Item", "Table,Item,Value")
            itemB (string): X-axis string, ("Table,Item,Type")
            step (int): Sets Step size, grouping N objects together. (0-3 for date fields)

        Returns:
            string: JSON String containing the result.
        """

        #TODO: WHERE
        
        # As a consequence of the JSON request, type and step will always be given as strings.
        # Here we conver them back into ints
        type = int(type)
        step = int(step)
        
        # Parse CSV input, temp var is the CSV parser
        temp = csv.reader([itemA], delimiter=',')
        
        # tempRow holds the parsed row
        tempRow = []
        
        # This for loop is basically the only documented way I could find 
        # to get data out of this , so a for loop it is. We save the row to tempRow.
        for row in temp:
            tempRow = row
            
        # We pull the row data out into discrete vars named 
        # so that the following code is easier for humans to parse.
        aTable = tempRow[0]
        aEntry = tempRow[1]
        
        # Length of itemA is variable, if statement to check for 
        # case where we pass three items.
        if len(tempRow) == 3 :
            aValue = tempRow[2]
        else:
            aValue = ""
        
        #same as above for item B    
        temp = csv.reader([itemB], delimiter=',')
        for row in temp:
            tempRow = row
            
        # No conditional, as itemB has a fixed number of items
        bTable = tempRow[0]
        bEntry = tempRow[1]
        bType = tempRow[2]
        
        # If items A and B are on different tables, then we will need to 
        # join them. We can call a function to generate a JOIN statement,
        # and pass that on to the final command string.
        if aTable != bTable :
            joinStr = DB.__join(aTable, bTable) + " "
        else :
            joinStr = aTable + " "    

        # I wish I could use a switch statement here...
        # Build aStr with the appropriate modifier.
        if type == -1: # NOP
            aStr = aTable + "." + aEntry + ", "
            bType = "NULL" # We are not grouping, and we cannot skip, so short out that part of the req.
        elif type == 0: # AVG
            # AVG(aTable.aEntry)
            aStr = "AVG(" + aTable + "." + aEntry + "), " 
        elif type == 1: # SUM
            aStr = "SUM(" + aTable + "." + aEntry + "), "
        else:
            # we don't know what we should do, kill it
            return jsonify("Failed to provide valid mode: " + type)
        
        # Build bStr, or portion of SQL query that selects for B, with appropriate modifier
        # Build tailStr, or portion of SQL query that groups/orders the data, tied to B's type.
        
        # if bType was set to NULL, then we are not grouping at all, so simply
        # set the bStr, and exit
        if bType == "NULL":
            bStr = bTable + "." + bEntry + " "
            tailStr = ""
        # Otherwise, check for date, and build the appropriate string.
        elif bType == "date":
            if step == 0: # Group by Year Month Day
                bStr = "EXTRACT(YEAR_MONTH_DAY FROM " + bTable + "." + bEntry + ") "
                tailStr = "GROUP BY EXTRACT(YEAR_MONTH_DAY FROM " + bTable + "." + bEntry + ") ORDER BY EXTRACT(YEAR_MONTH_DAY FROM "  + bTable + "." + bEntry + ")"
            elif step == 1: # Group by Year Month
                bStr = "EXTRACT(YEAR_MONTH FROM " + bTable + "." + bEntry + ") "
                tailStr = "GROUP BY EXTRACT(YEAR_MONTH FROM " + bTable + "." + bEntry + ") ORDER BY EXTRACT(YEAR_MONTH FROM " + bTable + "." + bEntry + ")"
            elif step == 2: # Group by Year
                bStr = "EXTRACT(YEAR FROM " + bTable + "." + bEntry + ") "
                tailStr = "GROUP BY EXTRACT(YEAR FROM " + bTable + "." + bEntry + ") ORDER BY EXTRACT(YEAR FROM " + bTable + "." + bEntry + ")"
                # NOTE: Is there utility to have Month-Day or Year-Day options?
            else: # out of range value got pushed somehow, error out.
                return jsonify("Invalid step provided for DATE datatype!")
        else: #TODO: General case.
            return jsonify("Failed to provide valid type for item B."  + itemB)
        
        #build string!
        comStr = "SELECT " + aStr + bStr + "FROM " + joinStr + tailStr
        
        result = DB.__execute_com(comStr)
        # Build SQL query as needed
        return jsonify(result)