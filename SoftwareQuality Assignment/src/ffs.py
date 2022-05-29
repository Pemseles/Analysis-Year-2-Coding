import consolemenus as cm
import database as db
import menuoptions as mo

if __name__ == '__main__':
    cm.SystemScreenLoop()

    # print statements for test purposes
    print("Printing members in db:")
    for i in db.SelectAllFromTable("Members"):
        print(i.GetInfo())
    print ("Printing users in db:")
    for j in db.SelectAllFromTable("Users"):
        print(j.GetInfo())