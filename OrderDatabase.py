#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.1.0"
"""

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=line-too-long
# pylint: disable=invalid-name

# Standard Python libraries
import sqlite3
import bcrypt
from typing import Optional

# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values 
    
# Internal modules
import GlobalConstants as GC

class OrderDatabase:
    """ Store non user identifable data in local SQLite database
    """
    FLOOR_PLAN_COLUMN_NUMBER = 1
    EXTERIOR_MATERIALCOLUMN_NUMBER = 2
    INTERIOR_COLOR_COLUMN_NUMBER = 3
    ROOF_STYLE_COLUMN_NUMBER = 4
    EXTRAS_COLUMN_NUMBER =5 
    EMAIL_COLUMN_NUMBER = 6

    def __init__(self, dbName='Order.db'):
        """ Constructor to initialize a OrderDatabase object
            Call db = OrderDatabase('Test.db') for testing
        
        Args:
            dbName (String): Filename of SQlite database, defaults to 'House.db'   
        """
        # Connect to the database
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()
        
        # Check if tables exist (using UserTable as placeholder for all tables) 
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ConfigurationTable'")
        if not self.cursor.fetchone():
            
            # Create four tables in House.db for user login and hardware state storage
            self.cursor.execute('''CREATE TABLE ConfigurationTable (id INTEGER PRIMARY KEY, floorplanType TEXT, exteriorMaterial TEXT, interiorColor TEXT, roofType TEXT, extras TEXT, email TEXT)''')
            self.cursor.execute('''CREATE TABLE UsersTable (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)''')

            # Create debuging logg
            self.cursor.execute('''CREATE TABLE DebugLoggingTable (id INTEGER PRIMARY KEY, variable TEXT)''')

            self.init_tables()
        
            # Create debuging logg
            self.cursor.execute('''CREATE TABLE DebugLoggingTable (id INTEGER PRIMARY KEY, variable TEXT)''')
            
        self.commit_changes()
    
    
    def init_tables(self):
        """ Initialize UserTable database for FUTURE WORK TODO
        """
        config = dotenv_values()
        username = config['DATABASE_ADMIN_USERNAME']
        password = config['DATABASE_ADMIN_PASSWORD']
        self.insert_users_table(username, password)
        
        self.commit_changes()


    def commit_changes(self):
        """ Commit data inserted into a table to the .db database file 
        """
        self.conn.commit()


    def close_database(self):
        """ Close database to enable another sqlite3 instance to query this House.db database
        """
        self.conn.close()


    def query_table(self, tableName: str, row: Optional[int]= None, column: Optional[int]= None) -> tuple:
        """ Return every row of a table from a *.db database OR a specific row or colum 

        Args:
            tableName (String): Name of table in database to query
            row (Interger): OPTIONAL row number to query 
            column (Interger): OPTIONAL column number to query 

        Returns:
            result: A list of tuples from a table, where each row in table is a tuple of length n
            isEmpty: Returns True if table is empty, and False otherwise
            isValid: Returns True is table name exists in MammothGPT.db, and False otherwise
            
        """
        try:
            sqlStatement = f"SELECT * FROM {tableName}"
            self.cursor.execute(sqlStatement)

            isEmpty = False
            isValid = True
            result = self.cursor.fetchall()
            if len(result) == 0:
                isEmpty = True

      
            if row == None and column == None:
                return result, isEmpty, isValid
            elif column == None:
                return result[row-1], isEmpty, isValid
            else:
                return result[row-1][column], isEmpty, isValid
                
        except IndexError:
            db.insert_debug_logging_table(f'Invalid table row or column number {row} OR {column} respectively was requested')
            return None, None, False
        
        except sqlite3.OperationalError:
            db.insert_debug_logging_table(f'The {tableName} table does NOT exist in Order.db or there is typo in table name')
            return None, None, False


    def insert_configuration_table(self, purchaseConfiguration: list, email: str) -> int:
    ###self.cursor.execute('''CREATE TABLE ConfigurationTable (id INTEGER PRIMARY KEY, floorplanType TEXT, exteriorMaterial TEXT, interiorColor TEXT, roofType TEXT, extras TEXT, email TEXT)''')
        
        (floorplanType, exteriorMaterial, interiorColor, roofType, extras) = purchaseConfiguration
        
        
        self.cursor.execute("INSERT INTO ConfigurationTable (floorplanType, exteriorMaterial, interiorColor, roofType, extras, email) VALUES (?, ?, ?, ?, ?, ?)", (floorplanType, exteriorMaterial, interiorColor, roofType, extras,  email))
        lastIdInserted = self.cursor.lastrowid
        self.commit_changes()   
        
        return lastIdInserted


    def update_configuration_table(self, id: int, newFanLevel: float):    
        """ Update FanLevelTable in database using a GlobalConstants.py CONSTANT 
            
        Args:
            id (Integer): Primary key in FanLevelTable to update 
            newFanLevel (Float): New fan rotation speed (OFF, LOW, MED, HIGH) for a single fan
        """
        self.cursor.execute("UPDATE FanLevelTable SET currentLevel = ? WHERE id = ?", (newFanLevel, id))
        self.commit_changes()


    def insert_debug_logging_table(self, debugVariable: str):
        self.cursor.execute("INSERT INTO DebugLoggingTable (variable) VALUES (?)", (debugVariable,))
        self.commit_changes()
        
        

    def insert_users_table(self, username: str, pw: str):
        """ Insert username, hashed password, and hash salt into the User Table if username is unqiue, otherwise update password

        Args:
            username (String): Username to login, which can be either a 10 digit phone number or email address
            pw (String): Password to login, which is NEVER stored as plain text in any database or on a SSD (RAM only)
        """
        results, foundUser = self.search_users_table(username)

        generatedSalt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(str(pw).encode('utf-8'), generatedSalt)

        if foundUser:
            idToUpdate = results[0][0]
            self.cursor.execute("UPDATE UsersTable SET username = ?, password = ?, salt = ? WHERE id = ?", (username, hashedPassword, generatedSalt, idToUpdate))
        else:
            self.cursor.execute("INSERT INTO UsersTable (username, password, salt) VALUES (?, ?, ?)", (username, hashedPassword, generatedSalt))

        self.commit_changes()


    def search_users_table(self, searchTerm: str) -> tuple:
        """ Search UsersTable table for every occurrence of a string

        Args:
            searchTerm (str): _description_

        Returns:
            List: Of Tuples from UsersTable, where each List item is a row in the table containing the exact search term
        """
        foundUser = False
        self.cursor.execute("SELECT * FROM UsersTable WHERE username LIKE ?", ('%' + searchTerm + '%',))
        results = self.cursor.fetchall()
        if len(results) > 0:
            foundUser = True
        
        return results, foundUser


    def verify_password(self, enteredUsername: str, enteredPassword: str) -> bool:
        """Vefify if username (phone number or email address) and password match 

        Args:
            enteredUsername (String): Santizied username input by a user into a GUI textbox
            enteredPassword (String): Raw password input by a user into a GUI textbox

        Returns:
            bool: True if salted hash password in database matches the password entered by the user, False otherwise
        """
        usersTableList, foundData =  self.query_table("UsersTable")
        isUserFound = False
        for user in usersTableList:
            if foundData:
                if user[OrderDatabase.USERNAME_COLUMN_NUMBER] == enteredUsername:
                    isUserFound = True

                    storedHashedPassword = user[OrderDatabase.PASSWORD_COLUMN_NUMBER]
                    storedSalt = user[OrderDatabase.SALT_COLUMN_NUMBER]
                    hashedPasssword = bcrypt.hashpw(enteredPassword.encode('utf-8'), storedSalt)

                    if hashedPasssword == storedHashedPassword:
                        return True
                    else:
                        return False
                else:
                    isUserFound = isUserFound or False


if __name__ == "__main__":
    print("Testing OrderDatabase.py with asserts")

    db = OrderDatabase('Test.db')

    
    db.insert_debug_logging_table("Testing debug logging")

    db.insert_users_table("blazes@mfc.us", "TestPassword")
    db.insert_users_table("blazes@mfc.us", "NewPassword")  # Test that duplicate usernames creates new password
    databaseSearch, foundUser = db.search_users_table("blazes@mfc.us")
    
    assert foundUser, "Search for know username in database failed"
    assert db.verify_password("blazes@mfc.us", "NewPassword"), "Password salted hashing failed"
    assert not db.verify_password("blazes@mfc.us", "BadPassword"), "Password salted hashing failed"

    db.close_database()
    