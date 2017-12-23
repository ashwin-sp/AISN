import MySQLdb
import datetime

sql = ""
db = MySQLdb.connect("localhost", "root", "root", "ashwin")
cursor = db.cursor()
print("So you want to check the performance of students is it? Fine then let's start with a number:")
print("1. Rating for the Student")
print("2. Tough Subject")
print("3. Teacher Rankings")
print("4. Salary")
print("5. Exit")

daycounter = datetime.datetime.today().day
db = MySQLdb.connect("localhost", "root", "root", "ashwin")
cursor = db.cursor()

if(daycounter % 20 == 0):
	sql = """update teacher set Salary = Salary+ 100* Diff"""
	cursor.execute(sql)

def choicer(choice):  
    if(choice == 1):
    	regger = int(input("Enter the Register number for which you need the rating"))
    	sql = "select Name, Regno, Dept, AVG(Marks) from student a, mark b where a.Register_number = b.Regno and a.Register_number = %d group by b.Regno" % (regger)
    	cursor.execute(sql)
    	result = cursor.fetchall()
    	Name = ""
    	Dept = ""
    	Average = 0
    	Passpercent = 0
    	for row in result:
    		Name = row[0]
    		Dept = row[2]
    		Average = row[3]
    	cursor.execute("drop table if exists pass2")
    	cursor.execute("drop table if exists total2")
    	sql = "CREATE table pass2 (pass INT) SELECT COUNT(*) as pass FROM mark WHERE Marks > 49 and Regno=%d" %(regger)
    	cursor.execute(sql)
    	sql = "CREATE table total2 (total INT) SELECT COUNT(*) as total FROM mark WHERE Regno=%d" %(regger)
    	cursor.execute(sql)
    	sql = """SELECT (pass2.pass * 100)/ (total2.total) FROM pass2, total2"""
    	cursor.execute(sql)
    	result= cursor.fetchall()
    	for row in result:
    		Passpercent = row[0]
    	db.commit()
    	print("The AISNdb rating of %s from %s is %f" % (Name, Dept, (Average+Passpercent)/20))
    elif(choice == 2):
    	depttough = input("Enter the department for which you need to know the tough subject")
    	cursor.execute("drop table if exists averager")
    	cursor.execute("drop table if exists pass3")
    	cursor.execute("drop table if exists total3")
    	cursor.execute("drop table if exists passer")
    	cursor.execute("drop table if exists subratingtable")
    	cursor.execute("create table averager (Sub VARCHAR(20), Avg INT) select Subject as Sub, AVG(Marks) as Avg from mark group by Subject")
    	cursor.execute("CREATE table pass3 (pass INT, Sub VARCHAR(50)) SELECT Subject as Sub, COUNT(*) as pass FROM mark WHERE Marks > 49 group by Subject")
    	cursor.execute("CREATE table total3 (total INT, Sub VARCHAR(50)) SELECT Subject as Sub, COUNT(*) as total FROM mark group by Subject")
    	cursor.execute("CREATE table passer(Sub VARCHAR(50), Passavg INT) SELECT pass3.Sub as Sub, (pass3.pass * 100)/ (total3.total) as Passavg FROM pass3, total3 where pass3.Sub = total3.sub")
    	cursor.execute("create table subratingtable (Sub VARCHAR(20), Point FLOAT) select passer.Sub as Sub, ((averager.Avg + passer.Passavg)/20) as Point from passer,averager where passer.Sub = averager.Sub")
    	cursor.execute("select * from subratingtable where Point = (select MIN(Point) from subratingtable a, mark b where a.Sub = b.Subject and b.Dept = '%s')" % (depttough))   	
    	result = cursor.fetchall()
    	for row in result:
    		print("The tough subject is %s with a rating of %f"%(row[0],row[1]))
    elif(choice ==3):
    	cursor.execute("drop table if exists pass5")
    	cursor.execute("drop table if exists total5")
    	cursor.execute("drop table if exists passer5")
    	cursor.execute("drop table if exists averager5")
    	cursor.execute("drop table if exists subratingtable5")
    	cursor.execute("create table averager5 (Emp VARCHAR(20), Avg INT) select Empno as Emp, AVG(Marks) as Avg from mark group by Empno")
    	sql = "CREATE table pass5 (pass INT, Emp VARCHAR(50)) SELECT COUNT(*) as pass, Empno as Emp FROM mark WHERE Marks > 49 group by Empno"
    	cursor.execute(sql)
    	cursor.execute("CREATE table total5 (total INT, Emp VARCHAR(50)) SELECT Empno as Emp, COUNT(*) as total FROM mark group by Empno")
    	cursor.execute("CREATE table passer5(Emp VARCHAR(50), Passavg INT) SELECT pass5.Emp as Emp, (pass5.pass * 100)/ (total5.total) as Passavg FROM pass5, total5 where pass5.Emp = total5.Emp")
    	cursor.execute("create table subratingtable5 (Emp VARCHAR(20), Point FLOAT) select passer5.Emp as Emp, ((averager5.Avg + passer5.Passavg)/20) as Point from passer5,averager5 where passer5.Emp = averager5.Emp")
    	cursor.execute("UPDATE teacher INNER JOIN subratingtable5 ON (teacher.Empid = subratingtable5.Emp) set teacher.Point = subratingtable5.Point")
    	cursor.execute("UPDATE teacher set Diff= teacher.Point/2")
    	cursor.execute("select a.Name, b.Emp, b.Point from teacher a, subratingtable5 b where a.Empid = b.Emp order by b.Point desc")
    	result = cursor.fetchall()
    	i = 0
    	for row in result:
    		i+=1
    		print("Position %d: %s ( AISNdb Rating: %d )" % (i, row[0], row[2]))
    elif(choice==4):
    	teacherr = int(input("Enter the teacher employee ID for which you need to know the salary:"))
    	sql = "select Name, Salary from teacher where Empid=%d" % (teacherr)
    	cursor.execute(sql)
    	result = cursor.fetchall()
    	for row in result:
    		print("The salary of %s is %d" % (row[0],row[1]))
    else:
        print("Not in range")
choice = int(input())
while(choice != 5):
    choicer(choice)
    print("1. Rating for the Student")
    print("2. Tough Subject")
    print("3. Teacher Rankings")
    print("4. Salary")
    print("5. Exit")
    choice = int(input())
db.close()
print("Bye")