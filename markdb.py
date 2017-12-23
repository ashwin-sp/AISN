import MySQLdb

sql = ""
db = MySQLdb.connect("localhost", "root", "root", "ashwin")
cursor = db.cursor()
print("Oye!!! master please be careful while uploading/updating marks. Choose the number corresponding to the task you want to work with")
print("1. Create a database for the new examination")
print("2. Add marks for a particular set of register numbers")
print("3. Updation")
print("4. Deletion")
print("5. Average marks")
print("6. Best mark")
print("7. Passing percentage")
print("8. Pass or fail")
print("9. Exit")

def choicer(choice):  
    if(choice == 1):
        try:
            sql = """drop table if exists mark"""   
            cursor.execute(sql)
            sql = """drop table if exists passstatus"""
            cursor.execute(sql)
            sql = """create table mark(Regno INT,Empno INT,Subject VARCHAR(20),Dept VARCHAR(50), Marks INT, FOREIGN KEY (Regno) REFERENCES student(Register_number), FOREIGN KEY(Empno) REFERENCES teacher(Empid))"""
            cursor.execute(sql)
            sql = """create table passstatus(Regisno INT,Empisno INT, Status VARCHAR(7),Dpt VARCHAR(50),FOREIGN KEY (Regisno) REFERENCES mark(Regno), FOREIGN KEY (Empisno) REFERENCES mark(Empno))"""
            cursor.execute(sql)
            print("Create has Succeeded")
            db.commit()
        except:
            print("Create has failed")
            db.rollback()
    elif(choice == 2):
        count = int(input("How many records do you want to insert?"))
        while(count>0):    
	        try:       
	            reg = int(input("Enter the student's register number:"))
	            teachreg = int(input("Enter the employee number of the assigned teacher:"))
	            sub = input("Enter the subject:")
	            dept = input("Enter the student's department:")
	            mark = int(input("Enter the mark obtained:"))
	            sql = "insert into mark values(%d,%d,'%s','%s',%d)" % (reg,teachreg,sub,dept,mark)
	            cursor.execute(sql)
	            print("I have uploaded the details successfully in the Database")
	        except:
	        	print("Teacher or Student does not exist")
	        count-=1
    elif(choice == 3):
        count = int(input("How many records do you want to update?"))
        while(count>0):
            reg = int(input("Enter the register number for which the mark has to be changed?"))
            sub = input("Enter the subject")
            new = int(input("Enter the new mark:"))
            try:
            	sql = "update mark set Marks = %d where Regno = %d and Subject = '%s'" % (new, reg, sub)
            	cursor.execute(sql)
            	print("Successfully updated master")
            	db.commit()
            except:
            	print("Update failed. Possible reason maybe due to missing data")
            count-=1   
    elif(choice == 4):
    	count = int(input("How many records do you want to delete?"))
    	while(count>0):
    		innerchoice = input("Do you want to delete the records 'department' wise, 'register' number wise, 'teacher' wise or 'subject' wise?")
    		if innerchoice == "department":
    			try:
    				deptdeleter = input("Enter the Department numbers of the record you want to delete")
    				sql = "delete from mark where Dept = '%s'" % (deptdeleter)
    				cursor.execute(sql)
    				print("Removed the record(s) successfully master")
    				db.commit()
    			except:
    				print("Deletion of department records failed")
    				db.rollback()
    		elif(innerchoice == "register"):
    			try:
    				regdeleter = int(input("Enter the number to delete"))
    				sql = "delete from mark where Regno = %d" % (regdeleter)
    				cursor.execute(sql)
    				print("Removed the record(s) successfully master")
    				db.commit()
    			except:
    				print("Deletion of records pertaining to a particular register number failed")
    				db.rollback()
    		elif(innerchoice == "teacher"):
    			try:
    				teachdeleter = int(input("Enter the employee ID for which all records are to be erased"))
    				sql = "delete from mark where Empno = %d" % (teacherdeleter)
    				cursor.execute(sql)
    				print("Removed the records successfully master")
    				db.commit()
    			except:
    				print("Deletion of records pertaining to a particular teacher failed")
    				db.rollback()
    		else:
    			try:
    				subdeleter = input("Enter the subject of the records for deletion")
    				sql = "delete from mark where Subject = '%s'" % (subdeleter)
    				cursor.execute(sql)
    				print("Removed the records successfully master")
    				db.commit()
    			except:
    				print("Deletion of department records failed")
    				db.rollback()
    		count-=1
    elif(choice == 5):
        innerchoice = input("Do you want the 'department' wise average, 'subject' wise average or the 'student' wise average?")
        if innerchoice == "department":
        	try:
        		sql = "select Dept, AVG(Marks) from mark group by Dept"
        		cursor.execute(sql)
        		result = cursor.fetchall()
        		print("Department\t")
        		for row in result:
        			print("%s\t" %(row[0]))
        		print("\nMark\t")
        		for row in result:
        			print("%d" % (row[1]))
        		db.commit();
        	except:
        		print("Results could not be fetched at this time, please try again later")
        		db.rollback();
        elif innerchoice == "subject":
        	try:
        		sql = "select Subject, AVG(Marks) from mark group by Subject"
        		cursor.execute(sql)
        		result = cursor.fetchall()
        		print("Subject\t")
        		for row in result:
        			print("%s\t" %(row[0]))
        		print("\nMark\t")
        		for row in result:
        			print("%d" % (row[1]))
        		db.commit();
        	except:
        		print("Results could not be fetched at this time, please try again later")
        		db.rollback();
        else:
        	inchoice = input("Do you want the average for 'some' or 'all' students?")
        	if inchoice == "some":
        		counter = int(input("Enter the number of records for which you want to see the average"))
        		while(counter>0):
        			regdisplayer = input("Enter the name for which you want to see the average?")
        			try:
        				sql = "select Name, Regno, Dept, AVG(Marks) from student a, mark b where a.Register_number = b.Regno and a.Name = '%s' group by b.Regno" % (regdisplayer)
        				cursor.execute(sql)
        				result = cursor.fetchall()
        				for row in result:
        					print("Name = %s" %(row[0]))
        					print("Regno = %d" % (row[1]))
        					print("Department = %s" % (row[2]))
        					print("Average = %d" %(row[3]))
        				db.commit()
        			except:
        				print("Result not available at this time, please try later")
        				db.rollback()
        			counter-=1
        	else:
        		try:
        			sql = "select Regno, AVG(Marks) from mark group by Regno"
        			cursor.execute(sql)
        			result = cursor.fetchall()
        			for row in result:
        				print("Regno = %d" % (row[0]))
        				print("Average = %d" % (row[1]))
        			db.commit()
        		except:
        			print("Result not available at this time, please try later")
        			db.rollback()
    elif(choice==6):
    	innerchoice = input("Select 'subject' or 'department' wise topper")
    	if(innerchoice == "subject"):
    		subjecter= input("Enter the subject")
    		sql = "SELECT Name, Register_number, Marks from student A, mark B where A.Register_number = B.Regno and B.Subject = '%s' and B.Marks = (select MAX(Marks) from mark group by Subject having Subject= '%s')" % (subjecter,subjecter)
    		cursor.execute(sql)
    		result = cursor.fetchall()
    		for row in result:
    			print("Name:'%s'" % (row[0]))
    			print("Register number:%d" % (row[1]))
    			print("Mark:%d" % (row[2]))
    		db.commit()    			
    	else:
    		deptopper = input("Enter the department")
    		sql = """drop view if exists totals"""
    		cursor.execute(sql)
    		sql = "CREATE VIEW totals AS SELECT Name AS totname, Register_number AS totreg, Dept AS totdept,SUM(Marks) AS total FROM student A, mark B where A.Register_number= B.Regno GROUP BY A.Register_number HAVING B.Dept = '%s'" % (deptopper)
    		cursor.execute(sql)
    		sql = "SELECT totname, totreg, total, totdept FROM totals where total = (SELECT MAX(total) from totals group by totdept having totdept= '%s')" % (deptopper)
    		cursor.execute(sql)
    		result = cursor.fetchall()
    		for row in result:
    			print("Name:'%s'" % (row[0]))
    			print("Register number:%d" % (row[1]))
    			print("Total:%d" % (row[2]))
    			print("Department:'%s'" % (row[3]))
    		db.commit()
    elif(choice == 7):
    	innerchoice = input("Do you want 'subject' passing percentage, 'teacher' wise passing percentage or the 'department' pass percentage?")
    	if innerchoice=="subject":
    		subpass = str(input("Enter the subject for which you require the passing percentage?"))
    		cursor.execute("drop table if exists pass")
    		cursor.execute("drop table if exists total")
    		sql = "CREATE table pass (pass INT) SELECT COUNT(*) as pass FROM mark WHERE Marks > 49 and Subject='%s'" %(subpass)
    		cursor.execute(sql)
    		sql = "CREATE table total (total INT) SELECT COUNT(*) as total FROM mark WHERE Subject='%s'" %(subpass)
    		cursor.execute(sql)
    		sql = """SELECT (pass.pass * 100)/ (total.total) FROM pass, total"""
    		cursor.execute(sql)
    		result= cursor.fetchall()
    		for row in result:
    			print("The passing percentage in '%s' is %d" % (subpass, row[0])) 
    	elif innerchoice == "teacher":
    		teachpass = int(input("Enter the teacher to know his or her production"))
    		cursor.execute("drop table if exists pass4")
    		cursor.execute("drop table if exists total4")
    		sql = "CREATE table pass4 (pass INT) SELECT COUNT(*) as pass FROM mark WHERE Marks > 49 and Empno=%d" % (teachpass)
    		cursor.execute(sql)
    		sql = "CREATE table total4 (total INT) SELECT COUNT(*) as total FROM mark WHERE Empno=%d" %(teachpass)
    		cursor.execute(sql)
    		sql = """SELECT (pass4.pass * 100)/ (total4.total) FROM pass4, total4"""
    		cursor.execute(sql)
    		result= cursor.fetchall()
    		for row in result:
    			print("The passing percentage produced is %d" % (row[0])) 
    	else:
    		deptpass = str(input("Enter the department for which you require the passing percentage?"))
    		cursor.execute("delete from passstatus")
    		cursor.execute("drop table if exists pass1")
    		cursor.execute("drop table if exists total1")
    		cursor.execute("INSERT into passstatus(Regisno,Dpt) SELECT DISTINCT Regno as Regisno,Dept as Dpt from mark")
    		cursor.execute("UPDATE passstatus INNER JOIN mark ON (Regisno = Regno) set Status = 'PASS' where mark.Marks > 49")
    		cursor.execute("UPDATE passstatus INNER JOIN mark ON (Regisno = Regno)set Status = 'FAIL' where mark.Marks < 50")
    		cursor.execute("CREATE table pass1 (pass INT) SELECT COUNT(*) as pass FROM passstatus WHERE Status = 'PASS' and Dpt = '%s'" %(deptpass))
    		cursor.execute("CREATE table total1 (pass INT) SELECT COUNT(*) as pass FROM passstatus WHERE Dpt = '%s'" %(deptpass))
    		cursor.execute("""SELECT (pass1.pass * 100)/ (total1.pass) FROM pass1, total1""")
    		result = cursor.fetchall()
    		for row in result:
    			print("The passing percentage in '%s' is %d" % (deptpass, row[0])) 
    elif(choice == 8):
    	regpass = int(input("Enter the register number for which you need the status"))
    	try:
    		cursor.execute("delete from passstatus")
    		sql = "INSERT into passstatus(Regisno) values(%d)" % (regpass)
    		cursor.execute(sql)
    		sql = "UPDATE passstatus INNER JOIN mark ON (Regisno = Regno) set Status = 'PASS' where mark.Marks > 49 and Regisno = %d" %(regpass)
    		cursor.execute(sql)
    		sql = "UPDATE passstatus INNER JOIN mark ON (Regisno = Regno)set Status = 'FAIL' where mark.Marks < 50 and Regisno = %d" % (regpass)
    		cursor.execute(sql)
    		sql = "SELECT * FROM passstatus WHERE Regisno = %d" % (regpass)
    		cursor.execute(sql)
    		result = cursor.fetchall()
    		for row in result:
    			print("He/she has %sED" %(row[2]))
    		db.commit()
    	except:
    		print("Result not released or no one has passed in the department")
    		db.rollback()
    else:
    	print("Not in range")
choice = int(input())
while(choice != 9):
    choicer(choice)
    print("1. Create a database for the new examination")
    print("2. Add marks for a particular set of register numbers")
    print("3. Updation")
    print("4. Deletion")
    print("5. Average marks")
    print("6. Best mark")
    print("7. Passing percentage")
    print("8. Pass or fail")
    print("9. Exit")
    choice = int(input())
db.close()
print("Bye")