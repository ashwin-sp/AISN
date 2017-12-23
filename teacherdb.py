import MySQLdb

sql = ""

print("What do you want to do master?")
print("1. Create a new dB of teachers")
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
        print("Inside choice 1")
        sql = """drop table if exists teacher"""   
        cursor.execute(sql)
        try:
            sql = """create table teacher(Name VARCHAR(50),Empid INT PRIMARY KEY,Dept VARCHAR(50), Subjects VARCHAR(50), Salary BIGINT, Diff INT, Point INT)"""
            cursor.execute(sql)
            print("Create has Succeeded")
            db.commit()
        except:
            print("Create has failed")
            db.rollback()
    elif(choice == 2 or choice == 1):
        count = int(input("How many records do you want to insert?"))
        while(count>0):
            try:
                name = input("Enter the teacher's name:")
                roll = int(input("Enter the teacher's employee number:"))
                dept = input("Enter the teacher's department:")
                sal = int(input("Enter the original assigned salary:"))
                sql = "insert into teacher(Name, Empid, Dept, Salary) values('%s',%d,'%s',%d)" % (name,roll,dept,sal)
                cursor.execute(sql)
                i = 0
                count_sub = int(input("Enter the number of subjects:"))
                while(count_sub>0):
                    subjects = input("Enter the %dth subject" % (i+1)) 
                    sql = "update teacher set Subjects = CONCAT(IFNULL(Subjects,''),'%s\n') where Empid = %d;" % (subjects,roll)
                    i+=1
                    cursor.execute(sql)
                    count_sub -= 1
                print("Insert was an success overall")
                db.commit()
            except:
                print("Insert failed")
                db.rollback()
            count-=1
    elif(choice == 3):
        count = int(input("How many records do you want to update?"))
        while(count>0):
            innerchoice = str(input("Do you want to update the 'name', 'employee' number, 'department', 'subjects' or 'salary' ?")).lower()
            if innerchoice == "name":
                try:
                    updater = int(input("Enter the Employee number for which you want to modify the name"))
                    newname = input("Enter the new name")
                    sql = "update teacher set Name = '%s' where Empid = %d" % (newname,updater)
                    cursor.execute(sql)
                    print("Updated successfully master")
                    db.commit()
                except:
                    print("Update on name failed")
                    db.rollback()
            elif innerchoice == "employee":
                try:
                    updater = input("Enter the Name for which you want to modify the employee number")
                    newreg = int(input("Enter the new employee number"))
                    sql = "update student set Empid = %d where Name = '%s'" % (newreg,updater)
                    cursor.execute(sql)
                    print("Updated successfully master")
                    db.commit()
                except:
                    print("Update on Register number failed")
                    db.rollback()
            elif innerchoice == "department":
                try:
                    updater = int(input("Enter the Employee number for which you want to modify the Department"))
                    new = input("Enter the new department")
                    sql = "update teacher set Dept = '%s' where Empid = %d" % (new,updater)
                    cursor.execute(sql)
                    print("Updated successfully master")
                    db.commit()
                except:
                    print("Update on department failed")
                    db.rollback()
            elif innerchoice == "subjects":
                try:
                    updater = int(input("Enter the Employee number for which you want to change the subjects"))
                    sql = "update teacher set Subjects = null where Empid = %d" %(updater)
                    newcounter = int(input("Enter the count of new subjects"))
                    i = 0
                    while(newcounter>0):
                        new = input("Enter the %dth subject" % (i+1))
                        sql = "update teacher set Subjects = CONCAT(IFNULL(Subjects,''), '%s\n') where Empid = %d;" % (new,updater)
                        cursor.execute(sql)
                        i+=1
                        newcounter-=1
                    print("Update was an success")
                    db.commit()
                except:
                    print("Update on subjects failed")
                    db.rollback()
            else:
                try:
                    updater = int(input("Enter the Employee number for which you want to modify the Department"))
                    new = int(input("Enter the new department"))
                    sql = "update teacher set Salary = %d where Empid = %d" % (new,updater)
                    cursor.execute(sql)
                    print("Successfully updated master")
                    db.commit()
                except:
                    print("Update on department failed")
                    db.rollback()
            count-=1   
    elif(choice == 4):
        count = int(input("How many records do you want to delete?"))
        while(count>0):
            try:
                regdeleter = int(input("Enter the Employee number of the record you want to delete"))
                sql = "delete from student where Empid = %d" % (regdeleter)
                cursor.execute(sql)
                print("Well that went easy for a deletion")
                db.commit()
            except:
                print("Delete with register number failed")
                db.rollback()
            count-=1
    elif(choice == 5):
        print("Still under construction so we will display all entries if available")
        try:
            sql = """select * from teacher"""
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print("Name = %s" %(row[0]))
                print("Employee ID = %d" % (row[1]))
                print("Department = %s" % (row[2]))
                print("Salary = %d" % (row[4]))
                print("Subjects = %s" % (row[3]))
                if(row[6] is None):
                    print("The rating is still not available\n")
                else:
                    print("AISNdb Rating: %d\n" % row[6])
            db.commit()
        except:
            print("Display failed")
            db.rollback()
    else:
        print("Not in range")
choice = int(input())
while(choice != 6):
    choicer(choice)
    print("1. Create a new dB of teachers")
    print("2. Add a new entry / entries")
    print("3. Update an entry / entries")
    print("4. Delete an entry / entries")
    print("5. Display 1 or more entries")
    print("6. Exit")
    choice = int(input())
db.close()
print("Bye")
