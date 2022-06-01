import email
from msilib.schema import Error

from numpy import isin
import dbclasses as dbc
import encryption as enc
from datetime import date
import sqlite3

def Create_Connection(db_file):
    # TODO: add logged-in-user authentication
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def CreateMemberTable():
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS Members (
            membership_id integer PRIMARY KEY,
            registration_date DATE NOT NULL,
            first_name text NOT NULL,
            last_name text NOT NULL,
            address text NOT NULL,
            email_address text NOT NULL UNIQUE,
            phone_number text NOT NULL
            ); """)

def CreateUserTable():
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS Users (
            id integer PRIMARY KEY AUTOINCREMENT,
            registration_date DATE NOT NULL,
            first_name text NOT NULL,
            last_name text NOT NULL,
            username text NOT NULL UNIQUE,
            password text NOT NULL UNIQUE,
            address text NOT NULL,
            email_address text NOT NULL UNIQUE,
            phone_number text NOT NULL,
            role integer NOT NULL,
            role_name text NOT NULL
            ); """) # role defines if user is Advisor (0), System Admin (1) or Super Admin (2)

def InsertIntoMembersTable(membership_id, registration_date, first_name, last_name, address, email_address, phone_number):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()

        # encrypt sensitive info
        first_name = enc.Encrypt(first_name)
        last_name = enc.Encrypt(last_name)
        address = enc.Encrypt(address)
        email_address = enc.Encrypt(email_address.lower())
        phone_number = enc.Encrypt(phone_number)

        c.execute(""" INSERT INTO Members (membership_id, registration_date, first_name, last_name, address, email_address, phone_number) 
            VALUES(?,?,?,?,?,?,?)""",(membership_id, registration_date, first_name, last_name, address, email_address, phone_number))

def InsertIntoUsersTable(registration_date, first_name, last_name, username, password, address, email_address, phone_number, role):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()

        # determine role_name
        role_name = ""
        if (role == 0):
            role_name = "Advisor"
        elif (role == 1):
            role_name = "System Administrator"
        elif (role == 2):
            role_name = "Super Administrator"
        
        # encrypt sensitive info
        first_name = enc.Encrypt(first_name)
        last_name = enc.Encrypt(last_name)
        username = enc.Encrypt(username.lower())
        password = enc.Encrypt(password)
        address = enc.Encrypt(address)
        email_address = enc.Encrypt(email_address.lower())
        phone_number = enc.Encrypt(phone_number)

        c.execute(""" INSERT INTO Users (registration_date, first_name, last_name, username, password, address, email_address, phone_number, role, role_name)
            VALUES(?,?,?,?,?,?,?,?,?,?)""",(registration_date, first_name, last_name, username, password, address, email_address, phone_number, role, role_name))

def DeleteFromTable(loggedInUser, target):
    # delete from table
    table = ""
    filterDigit = 0
    filter = ""
    # check if target is member or user
    if isinstance(target, dbc.Members):
        if not loggedInUser.role == 0 and not loggedInUser.role == 1 and not loggedInUser.role == 2:
            # logged in user is not authorized to delete member
            # LOG: sus
            return "Not authorized to delete member."
        table = "Members"
        filterDigit = target.membership_id
        filter = "membership_id"
    elif isinstance(target, dbc.Users):
        if loggedInUser.role <= target.role and loggedInUser.role > 0 and loggedInUser.role < 3:
            # logged in user is not authorized to delete user
            # LOG: sus
            return "Not authorized to delete user."
        table = "Users"
        filterDigit = target.id
        filter = "id"
    # preceed with deleting target
    with Create_Connection("database.db") as db:
        c = db.cursor()
        print("deleting from table...")

        # fill sql statement with table, filter and filterDigit & execute
        c.execute(f"""DELETE FROM {table} WHERE {filter}={filterDigit}""")
        db.commit()

# only here for testing purposes & convenience
def InsertStaticUsers():
    # insert static super admin (change back username to superadmin & password to Admin321!)
    InsertIntoUsersTable(date.today().strftime("%d-%m-%y"), "Super", "Admin", "sa", "sa", "Someplace", "super@admin.com", "+31-6-12345678", 2)
    
    # insert static system admin (TODO: remove before delivering)
    InsertIntoUsersTable(date.today().strftime("%d-%m-%y"), "System", "Admin", "systemadmin", "System321!", "Someotherplace", "system@admin.com", "+31-6-87654321", 1)

    # insert static advisor (TODO: remove before delivering)
    InsertIntoUsersTable(date.today().strftime("%d-%m-%y"), "Ad", "Visor", "advisor", "Advisor321!", "Somerandomplace", "ad@visor.com", "+31-6-11111111", 0)

def ConvertFetchToArray(fetched):
    newArr = []
    for i in fetched:
        newArr.append(list(i)[0])
    return newArr

def SelectAllFromTable(table_name):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute(f"""SELECT * FROM {table_name}""")
        rows = c.fetchall()
        for i in range(len(rows)):
            if (table_name == "Members"):
                rows[i] = dbc.Members(*rows[i])
            elif (table_name == "Users"):
                rows[i] = dbc.Users(*rows[i])
        return rows

def SelectColumnFromTable(table_name, column_name):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute(f"""SELECT {column_name} FROM {table_name}""")
        rows = c.fetchall()
        return rows

def SelectFilterUsersTable(column, filter):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute(f"""SELECT * FROM Users WHERE {column} = {filter}""")
        rows = c.fetchall()
        for i in range(len(rows)):
            rows[i] = dbc.Users(*rows[i])
        return rows

def SelectFilterMembersTable(column, filter):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute(f"""SELECT * FROM Members WHERE {column} = {filter}""")
        rows = c.fetchall()
        for i in range(len(rows)):
            rows[i] = dbc.Members(*rows[i])
        return rows

def UpdateUserEntry(newEntry):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute(""" UPDATE Users 
                    SET first_name = ? , 
                        last_name = ? , 
                        username = ? , 
                        password = ? , 
                        address = ? , 
                        email_address = ? , 
                        phone_number = ? 
                    WHERE id = ?""", newEntry)
        db.commit()

def UpdateMemberEntry(newEntry):
    # TODO: add logged-in-user authentication
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute("""UPDATE Members SET first_name = ? , last_name = ? , address = ? , email_address = ? , phone_number = ? WHERE membership_id = ?""", newEntry)
        db.commit()

if __name__ == '__main__':
    with Create_Connection("database.db") as db:
        c = db.cursor()
        c.execute("""DROP TABLE Members""")
        c.execute("""DROP TABLE Users""")
    CreateMemberTable()
    CreateUserTable()
    InsertStaticUsers()

    # print statements for test purposes
    print("Printing members in db:")
    for i in SelectAllFromTable("Members"):
        print(i.GetInfo2())
    print ("Printing users in db:")
    for j in SelectAllFromTable("Users"):
        print(j.GetInfo2())