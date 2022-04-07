# Functions for interacting with the database.
# TODO: Put this in a class without breaking it

from logging import addLevelName
from flask import current_app, g, jsonify
import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
import json
import csv

class DB(object):
    tunnel=None
    connection=None
    db_user=None
    db_password=None
    database=None
    def __init__(self, 
                db_user=None, 
                db_password=None, 
                schema=None, 
                ssh_user=None, 
                ssh_password=None, 
                host=None, 
                port=None):
        if ssh_user != None:
            self.setSSH(user=ssh_user,
                        password=ssh_password,
                        host=host,
                        port=port)
        self.setDB(user=db_user,
                   password=db_password,
                   schema=schema)
        if ssh_user != None:
            self.connect(port=self.tunnel.local_bind_port)
        else:
            self.connect(port=3306)
        return
    
    def __del__(self):
        self.tunnel.close()
        return
    
    def setSSH(self, user=None, password=None, host=None, port=None):
        self.tunnel
        if host != None:
            self.tunnel = SSHTunnelForwarder(
                (host, int(port)),
                ssh_username = user,
                ssh_password = password,
                remote_bind_address = ('localhost', 3306)
            )
        self.tunnel.start()
        return
    
    def setDB(self, user=None, password=None, schema=None):
        self.db_user=user
        self.db_password=password
        self.database=schema
        return
        
    def connect(self, port=None):
        #try:
        self.connection = pymysql.connect( user=self.db_user
                                    , password=self.db_password
                                    , host='localhost'
                                    , database=self.database
                                    , port=port)
        # except pymysql.connector.Error as e:
        #     print("Error code:", e.errno)        # error number
        #     print("SQLSTATE value:", e.sqlstate) # SQLSTATE value
        #     print("Error message:", e.msg)       # error message
        #     print("Error:", e)                   # errno, sqlstate, msg values
        #     s = str(e)
        #     print("Error:", s)                   # errno, sqlstate, msg values
        return
    
    def disconnect(self):
        self.connection.close()
        return
    
    def execute_com(self, string="", commit=False):
        """ Takes a given string, assuming it is a valid SQL Query, and executes it.

        Args:
            string (string): SQL Query

        Returns:
            type: description (it's complicated, I'll sort it out this weekend?)
        """
        #TODO: Fill out return fields in docstring
        #TODO: Implement error handling for mysql connection.
        #self.connection.autoCommit = True
        cur = self.connection.cursor()
        try:
            items = cur.execute(string)
            if commit:
                self.connection.commit()
        except:
            self.connection.rollback()
        #self.connection.autoCommit = False
        
        items = cur.fetchall()
        
        return items 
       
    def join(self, tableA=None, tableB=None):
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
        keyA = self.execute_com(command1)
        keyB = self.execute_com(command2)
        
        # Check table B for key A.
        for x in range(0, len(keyA)):
            if keyA[x][0] == tableB:
                # If we find it, set KeyA
                keyA = keyA[x][1]
                break
                
        # Check table A for key B
        for y in range(0, len(keyB)):
            if keyB[y][0] == tableA:
                keyB = keyB[y][1]
                break
        
        # if keyA returned empty
        if (keyA == []):
            #then we use keyB
            command = tableA + " JOIN " + tableB + \
            " ON " + tableB + "." + keyB + " = " + tableA + "." + keyB + " "
        else:
            #otherwise, we use keyA
            command =  tableA +" JOIN " + tableB + \
            " ON " + tableA + "." + keyA + " = " + tableB + "." + keyA + " "
        ## TODO: Throw error on failure   
        return command  
    
    def get_table_list(self):
        """ Gets a list of all tables in the schema.
        
        NOTE: I don't think this is used.

        Returns:
            string: JSON list of all tables in the schema
        """
        command = "SHOW TABLES"
        items = self.execute_com(command)
        return items

    def get_table_columns(self, table=None):
        """Gets a list of all columns in a table.

        Args:
            table (string): A table in the current schema.

        Returns:
            string : JSON list of all columns in the table.
        """
        command = "SHOW COLUMNS FROM " + table
        items = self.execute_com(command)
        return items

    
    def get_all(self):
        """ Queries the database for all fields.

        Returns:
            string: A JSON String containing {"table_name", "item_name", "item_type"}
        """
        items = self.get_table_list()
        cols = 0
        result = []
        for x  in range(0, len(items)):
            # string is padded, cut off the first three and last two chars
            cols =self.get_table_columns(table=str(items[x])[2:-3])
            for y in range(0, len(cols)):
                # append 2d array element with table name, item name and item type, in that order
                result.append([str(items[x])[2:-3], str(cols[y][0]), str(cols[y][1])[2:-1]])
        return json.dumps(result)   
        
        
class DBData(DB):
    def filterParse(self, comStr=None):
        fullArr = []
        andArr = comStr.split("&")
        for x in range(0, len(andArr)-1):
            if (andArr[x][0][-1] != '^') and (x != len(andArr)):
                andArr[x] += '&'
        for andCom in andArr:
            fullArr.append(andCom.split("^"))
        for x in range(0, len(fullArr[0])-1):
            if (fullArr[0][x][-1] != '&') and (x != len(fullArr)):
                fullArr[0][x] += '^'
        return fullArr
    


    
    def request(self, type=None, itemA=None, itemB=None, Filter=None, step=None):
        """ This function returns the JSON formatted results of an abstracted SQL request.

        The abstraction currently relies on a few core assumptions. We will only be returning two fields per request, and we will only average or sum the requests. The current syntax is designed so that it can be extended.
        
        The structure is as follows: TYPE, ITEMA, ITEMB, STEP
        
        TYPE is an enum that determines what operation is performed on the selected data. Pass -1 for no operation (this disables STEP), 0 for AVG, and 1 for SUM.
        
        ITEMA is the data we wish to view, and it is given as a CSV string containing either two ("Table,Item") or three ("Table,Item,Value") items. In order, these define the table the item exists in, the item's field, and if supplied, what value we are looking for.
        
        ITEMB is our scale/y-axis, given as a CSV string. It should contain exactly three items ("Table,Item,Type"). The rationale here is slightly different, as since we are using this entry to determine scale, the relevant SQL syntax is type dependent. We will not be searching for a given value here.
        
        Finally, STEP. This value is used to change the granularity of the input. With very large databases, it might be expected that several hundred thousand results may come back for a given query, leading to a response in the order of hundreds of megabytes. This puts an undue strain on the web-server, the network and the web application for little or no gain. So, increasing the STEP size will decrease the granularity of the data.

        Note on the Filter argument. The filter is the implemented interface for SQL WHERE statements. We can pass multiple filter arguments using '&'(AND) and '^'OR joiners.
        EX. "employees.gender.F.0^employees.gender.M.0"
        There shouldn't be a limit on how many objects can be filtered with this command. If you experience issues, make a github issue.
        
        The COMP option is passed as an integer value, because python thinks enums are silly. Values are as follows:
        0:= - Is equal to.
        1:<= - Is less than or equal to.
        2:< - Is strictly less than.
        3:> - Is strictly greater than.
        4:>= - Is greater than or equal to.
        5:! - Is not.

        Args:
            type (int): Operation type, (-1=NOP, 0=AVG, 1=SUM)
            itemA (string): Y-axis string, ("Table,Item")
            itemB (string): X-axis string, ("Table,Item,Type")
            Filter (string): Row filter string ("Table,Item,Value,COMP(&/^)Table,Item,...)
            NOTE: Comparitors other than 0 unimplemented
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
        
        #same as above for item B    
        temp = csv.reader([itemB], delimiter=',')
        for row in temp:
            tempRow = row
            
        # No conditional, as itemB has a fixed number of items
        bTable = tempRow[0]
        bEntry = tempRow[1]
        bType = tempRow[2]

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
           
        whereStr = "" # Holds generated WHERE statement
        
        # Put this here because WHERE statement can call outside tables.
        joinStr = "" # Holds generated JOIN statement
        tableArr = [] # Holds list of tables
        
        # If items are on different tables, then we will need to 
        # join them. We can call a function to generate a JOIN statement,
        # and pass that on to the final command string.
        if aTable != bTable :
            tableArr.append(aTable)
            # best-case no filters from other tables
            joinStr += self.join(aTable, bTable)
        if aTable == bTable :
            tableArr.append(bTable)
            joinStr += aTable + " "
        
        # If Filter is non-empty, Parse CSV
        if Filter != "":
            temp = self.filterParse(Filter)
            whereStr = "WHERE "
            for command in temp: 
                for x in range(0, len(command)):
                    temp = csv.reader([command[x]], delimiter=',')
                    for row in temp:
                        tempRow = row
                        
                    filterTable = tempRow[0]
                    filterItem = tempRow[1]
                    filterValue = tempRow[2]
                    # Clean up last value if opeartor is included
                    if (tempRow[3][-1:] == '&' or tempRow[3][-1:] == '^'):
                        filterType = int(tempRow[3][:-1])
                    else:
                        filterType = int(tempRow[3])
                
                    if filterType == 0:
                        whereStr += filterTable + "." + filterItem +  " = \"" + filterValue + "\" "
                    elif filterType == 1:
                        whereStr += filterTable + "." + filterItem +  " <= \"" + filterValue + "\" "
                    elif filterType == 2:
                        whereStr += filterTable + "." + filterItem +  " < \"" + filterValue + "\" "
                    elif filterType == 3:
                        whereStr += filterTable + "." + filterItem +  " > \"" + filterValue + "\" "
                    elif filterType == 4:
                        whereStr += filterTable + "." + filterItem +  " >= \"" + filterValue + "\" "
                    elif filterType == 5:
                        whereStr += filterTable + "." + filterItem +  " <> \"" + filterValue + "\" "
                    else:
                        return jsonify("Unsupported filterType on filter:", command[0])
                    
                    if (tempRow[3][-1:] == '&'):
                        whereStr += "AND "
                    elif (tempRow[3][-1:] == '^'):
                        whereStr += "OR "
                    # else do nothing
                    
                    # Add table to tableArr if needed
                    if filterTable not in tableArr:
                        tableArr.append(filterTable)
                        # clear best-case join
                        joinStr = ""
        else:
            whereStr = ""
            

        for x in range(1, len(tableArr)):
            joinStr += self.join(tableArr[0], tableArr[x])
            ## TODO: Try all combinations on successive errors.

        
        #HANDLE JOIN ACROSS SEPERATE TABLES
        #build string!
        comStr = "SELECT " + aStr + bStr + "FROM " + joinStr + whereStr +  tailStr
        
        print("Executing: ", comStr)
        
        result = self.execute_com(comStr)
        # Build SQL query as needed
        return jsonify(result)
    
class DBUser(DB):
    def __init__(self):
        super(DBUser, self).__init__(db_user="data"
                                   , db_password="Cg39rbaioxskMF4WyEfSfvbH"
                                   , host="localhost"
                                   , schema="DataVisUser"
                                   , port="3306")
        return
        
    def __del__(self):
        return
        
    def SearchUser(self, username=None, email=None):
        command = "SELECT "
        if username == None:
            command += "user_UUID, email, salt, secret FROM userLogin WHERE email = '" + email + "'"
        else:
            command += "user_UUID, username, salt, secret FROM userLogin WHERE username = '" + username + "'"

        result = self.execute_com(command)
        return result