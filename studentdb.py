import MySQLdb

sql = ""
print("Well not a bad time to start the day checking the student records. Pick a suitable number")
print("What do you want to do master?")
print("1. Create a new dB of students")
print("2. Add a new entry / entries")
print("3. Update an entry / entries")
print("4. Delete an entry / entries")
print("5. Display 1 or more entries")
print("6. Exit")

count = 0
db = MySQLdb.connect("localhost", "root", "root", "ashwin")
cursor = db.cursor()
    
def choicer(choice):  
    if(choice == 1):
        try:
            print("Inside choice 1")
            sql = """drop table if exists student"""   
            cursor.execute(sql)
            sql = """create table student(Name VARCHAR(50), Register_number INT PRIMARY KEY)"""
            cursor.execute(sql)
            print("Create has succeeded")
            db.commit()
        except:
            print("Create has failed")
            db.rollback()
    elif(choice == 2 or choice == 1):
        count = int(input("How many records do you want to insert?"))
        while(count>0):
            try:
                name = input("Enter the student's name:")
                roll = int(input("Enter the register number:"))
                sql = "insert into student values('%s',%d)" % (name,roll)
                cursor.execute(sql)
                print("I have inserted values in the database successfully master")
                db.commit()
            except:
                print("Insert failed")
                db.rollback()
            count-=1
    elif(choice == 3):
        count = int(input("How many records do you want to update?"))
        while(count>0):
            innerchoice = str(input("Do you want to change the name or rollno of student?")).lower()
            if innerchoice == "name":
                try:
                    nameupdater = int(input("Enter the register number for which you want to modify the name"))
                    newname = input("Enter the new name")
                    sql = "update student set Name = '%s' where Register_number = %d" % (newname,nameupdater)
                    cursor.execute(sql)
                    print("Update was successful master")
                    db.commit()
                except:
                    print("Update on name failed")
                    db.rollback()
            else:
                try:
                    regupdater = input("Enter the Name for which you want to modify the register number")
                    newreg = int(input("Enter the new register number"))
                    sql = "update student set Register_number = %d where Name = '%s'" % (newreg,regupdater)
                    cursor.execute(sql)
                    print("Update was successful master")
                    db.commit()
                except:
                    print("Update on Register number failed")
                    db.rollback()
            count-=1   
    elif(choice == 4):
        count = int(input("How many records do you want to delete?"))
        while(count>0):
            innerchoice = str(input("Do you want to delete by name or rollno of student?")).lower()
            if innerchoice == "name":
                try:
                    namedeleter = input("Enter the Name of the record you want to delete")
                    sql = "delete from student where Name = '%s'" % (namedeleter)
                    cursor.execute(sql)
                    print("Deleted without a fuss")
                    db.commit()
                except:
                    print("Delete with name failed")
                    db.rollback()
            else:
                try:
                    regdeleter = int(input("Enter the Register number of the record you want to delete"))
                    sql = "delete from student where Register_number = '%s'" % (regdeleter)
                    cursor.execute(sql)
                    print("Deleted without a fuss")
                    db.commit()
                except:
                    print("Delete with register number failed")
                    db.rollback()
            count-=1
    elif(choice == 5):
        outerinnerchoice = input("Do you want to display 'some' or 'all' records?")
        if outerinnerchoice == "some":
            count = int(input("How many records do you want to display?"))
            while(count>0):
                innerchoice = str(input("Do you want to display by 'name' or 'rollno' of student?")).lower()
                if innerchoice == "name":
                    try:
                        namedisplayer = input("Enter the Name of the record you want to display")
                        sql = "select * from student where Name = '%s'" % (namedisplayer)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        for row in result:
                            print("Name = '%s'" %(row[0]))
                            print("Register Number = %d" % (row[1]))
                        db.commit()
                    except:
                        print("Display with name failed")
                        db.rollback()
                else:
                    try:
                        regdisplay = int(input("Enter the Register number of the record you want to display"))
                        sql = "select * from student where Register_number = %d" % (regdisplay)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        for row in result:
                            print("Name = '%s'" %(row[0]))
                            print("Register Number = %d" % (row[1]))
                        db.commit()
                    except:
                        print("Display with register number failed")
                        db.rollback()
                count-=1
        else:
            print("We will display all entries if available")
            try:
                sql = """select * from student"""
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Name = '%s'" %(row[0]))
                    print("Register Number = %d" % (row[1]))
                db.commit()
            except:
                print("Display failed")
                db.rollback()
    else:
        print("Not in range")

choice = int(input())
while(choice != 6):
    choicer(choice)
    print("What do you want to do master?")
    print("1. Create a new dB of students")
    print("2. Add a new entry / entries")
    print("3. Update an entry / entries")
    print("4. Delete an entry / entries")
    print("5. Display 1 or more entries")
    print("6. Exit")
    choice = int(input())
db.close()
print("Bye")
