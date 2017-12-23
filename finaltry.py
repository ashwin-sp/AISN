from flask import Flask, render_template, json, request
from nltk import wordpunct_tokenize
from flask.ext.mysqldb import MySQL
import random
import MySQLdb
import re
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ashwin'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

stringer = ""
db = MySQLdb.connect("localhost", "root", "root", "ashwin")
cursor = db.cursor()
ultiflag = 0
flag = 0
@app.route("/")
def main():
	says = ["Hello !!!", "Hi, How are you?","Hey, How are you doing?","Hi, How have you been?"]
	result = random.choice(says)
	return "<h1><a href='/home'>"+result+"</a></h1>"
@app.route("/home")
def home():
	return render_template('mainer.html')
@app.route('/final',methods=['POST','GET'])
def message():
    if request.method == 'POST':
        app.logger.debug(" entered message function"+ request.form['query'])
        q = request.form['query']
        replierlist = wordpunct_tokenize(q)
        for reply in replierlist:
        	if reply in ["hi","hello","good morning","good afternoon","good evening","good"]:
        		return "Well that's good let's get rolling"+"<br>"+"<a href='/speak'> Display </a>"
        	else:
        		return "<br>hmm anyways let's start"+"<br>"+"<a href='/speak'> Display </a>"
@app.route('/test')
def test():
	cursor.execute("select * from student")
	data = cursor.fetchall()
	strr = ""
	for row in data:
		strr += row[0]+" "+str(row[1])+""" """
	return strr
@app.route('/speak')
def speaker():
	return render_template('webspeechdemo.html')
@app.route('/linker')
def linker():
	live = request.args.get('live')
	live = live.lower()
	replierlist = list(set(wordpunct_tokenize(live)))
	print(replierlist)
	ultiflag = 0
	stringer = ""
	for reply in replierlist:
		if reply in ["hi","hello","good morning","good afternoon","good evening","good"]:
			replierlist.remove(reply)
			ultiflag = 1
			stringer += "<br>Well that's good let's get rolling<br>"
		if reply in ["password"]:
			print(replierlist)
			ultiflag = 1 
			for reply in replierlist:
			    namelister = []
			    reglister = []
			    sublister = []
			    deptlister = []
			    teachlister = []
			    cursor.execute("select * from student")
			    result = cursor.fetchall()
			    for row in result:
			    	namelister.append(row[0])
			    	reglister.append(str(row[1]))
			    cursor.execute("select distinct Subject from mark")
			    result = cursor.fetchall()
			    for row in result:
			    	sublister.append(row[0].lower())
			    cursor.execute("select distinct Dept from mark")
			    result = cursor.fetchall()
			    for row in result:
			    	deptlister.append(row[0].lower())
			    cursor.execute("select distinct Empno from mark")
			    result = cursor.fetchall()
			    for row in result:
			    	teachlister.append(str(row[0]))
			    if reply in ["student","students"]:
			    	flag = 1 
			    	for reply in replierlist:
			    		if reply in ["details","detail","information"]:
			    			subflag = 0 
			    			for reply in replierlist:
			    				if  reply in namelister:
			    					subflag = 1
			    					cursor.execute("select Name,Regno,Subject,Dept,Marks from student a, mark b where a.Register_number = b.Regno and a.Name = '%s'" %(reply))
			    					result = cursor.fetchall()
			    					stringer += "<div class=""table-responsive""><table class=""table table-hover""><thead><tr><th>Name</th><th>Register Number</th><th>Subject</th><th>Department</th><th>Marks</th></tr></thead><tbody>"
			    					for row in result:
			    						stringer += "<tr><td>"+row[0].title()+"</td><td>"+str(row[1])+"</td><td>"+row[2]+"</td><td>"+row[3]+"</td><td>"+str(row[4])+"</td></tr>"
			    					stringer += "</tbody></table></div><hr>"
			    				if reply in reglister:
			    					subflag = 1
			    					cursor.execute("select * from mark where Regno = %d"%(int(reply)))
			    					result = cursor.fetchall()
			    					stringer += "<div class=""table-responsive""><table class=""table table-hover""><thead><tr><th>Register Number</th><th>Subject</th><th>Department</th><th>Marks</th></tr></thead><tbody>"
			    					for row in result:
			    						stringer += "<tr><td>"+str(row[0])+"</td><td>"+row[2]+"</td><td>"+row[3]+"</td><td>"+str(row[4])+"</td></tr>"
			    					stringer += "</tbody></table></div><hr>"
		    				if subflag == 0:
		    					cursor.execute("select * from mark")
		    					result = cursor.fetchall()
		    					stringer += "<br>The recently published results<br>"
		    					stringer += "<div class=""table-responsive""><table class=""table table-hover""><thead><tr><th>Register Number</th><th>Subject</th><th>Department</th><th>Marks</th></tr></thead><tbody>"
		    					for row in result:
		    						stringer += "<tr><td>"+str(row[0])+"</td><td>"+row[2]+"</td><td>"+row[3]+"</td><td>"+str(row[4])+"</td></tr>"
		    					stringer += "</tbody></table></div><hr>"
		    				subflag = 0
			    		if reply in ["average","averages"]:
			    			sql = "select Regno, AVG(Marks) from mark group by Regno"
			    			cursor.execute(sql)
			    			result = cursor.fetchall()
			    			for row in result:
			    				stringer += "<br>"+ str(row[0])+ " has overall average of "+ str(row[1])+"<br>"
			    if reply in ["teacher","teachers","professor"]:
			    	flag = 1 
			    	for reply in replierlist:
			    		if reply in ["percentage","percent"]:
			    			subfla = 0
			    			for reply in replierlist:
			    				if reply in teachlister:
			    					subflag = 1 
			    					cursor.execute("drop table if exists pass4")
			    					cursor.execute("drop table if exists total4")
			    					sql = "CREATE table pass4 (pass INT) SELECT COUNT(*) as pass FROM mark WHERE Marks > 49 and Empno=%d" % (int(reply))
			    					cursor.execute(sql)
			    					sql = "CREATE table total4 (total INT) SELECT COUNT(*) as total FROM mark WHERE Empno=%d" %(int(reply))
			    					cursor.execute(sql)
			    					sql = """SELECT (pass4.pass * 100)/ (total4.total) FROM pass4, total4"""
			    					cursor.execute(sql)
			    					result= cursor.fetchall()
			    					for row in result:
			    						stringer += "<br>The passing percentage produced by "+reply+" is "+str(row[0])+"<br>"
			    			if subfla == 0:
			    				cursor.execute("drop table if exists pass4")
			    				cursor.execute("drop table if exists total4")
			    				sql = "CREATE table pass4 (pass INT, Emp INT) SELECT COUNT(*) as pass, Empno as Emp FROM mark WHERE Marks > 49 GROUP BY Empno"
			    				cursor.execute(sql)
			    				sql = "CREATE table total4 (total INT, Emp INT) SELECT COUNT(*) as total, Empno as Emp FROM mark GROUP BY Empno" 
			    				cursor.execute(sql)
			    				sql = """SELECT distinct (pass4.pass * 100)/ (total4.total), Empno FROM pass4, total4,mark where pass4.Emp = total4.Emp and total4.Emp = mark.Empno"""
			    				cursor.execute(sql)
			    				result= cursor.fetchall()
			    				for row in result:
			    					stringer += "<br>The passing percentage produced by "+str(row[1])+ " is"+str(row[0])+"<br>"
			    			subfla = 0
			    		if reply in ["salary", "takeaway","amount","fee"]:
			    			subflag = 0 
			    			for reply in replierlist:
			    				if reply in teachlister:
			    					subflag = 1 
			    					sql = "select Name, Salary from teacher where Empid=%d" % (int(reply))
			    					cursor.execute(sql)
			    					result = cursor.fetchall()
			    					for row in result:
			    						stringer += "<br> The salary of "+row[0].title()+" is "+str(row[1])+"<br>" 
			    			if subflag == 0:
			    				sql = "select Name, Salary from teacher"
			    				cursor.execute(sql)
			    				result = cursor.fetchall()
			    				for row in result:
			    					stringer += "<br> The salary of "+row[0].title()+" is "+str(row[1])+"<br>"
			    			subflag = 0 
			    if reply in ["departments", "department"]:
			    	flag = 1
			    	for reply in replierlist:
			    		if reply in ["average","averages"]:
			    			subflag = 0 
			    			for reply in replierlist:
			    				if reply in deptlister:
			    					reply = reply.upper()
			    					subflag = 1 
			    					sql = "select Dept, AVG(Marks) from mark group by Dept having Dept = '%s'" % (reply)
			    					cursor.execute(sql)
			    					result = cursor.fetchall()
			    					for row in result:
			    						stringer += "<br>The average of "+row[0]+" is "+str(row[1])+"<br>"
			    			if subflag == 0:
			    				sql = "select Dept, AVG(Marks) from mark group by Dept"
			    				cursor.execute(sql)
			    				result = cursor.fetchall()
			    				for row in result:
			    					stringer += "<br>The average of "+row[0]+" is "+str(row[1])+"<br>"
			    			subflag = 0 
			    		if reply in ["topper","first"]:
			    			subflag = 0
			    			for reply in replierlist:
			    				if reply in deptlister:
			    					subflag = 1 
			    					reply = reply.upper()
			    					sql = """drop view if exists totals"""
			    					cursor.execute(sql)
			    					sql = "CREATE VIEW totals AS SELECT Name AS totname, Register_number AS totreg, Dept AS totdept,SUM(Marks) AS total FROM student A, mark B where A.Register_number= B.Regno GROUP BY A.Register_number HAVING B.Dept = '%s'" % (reply)
			    					cursor.execute(sql)
			    					sql = "SELECT totname, totreg, total, totdept FROM totals where total = (SELECT MAX(total) from totals group by totdept having totdept= '%s')" % (reply)
			    					cursor.execute(sql)
			    					result = cursor.fetchall()
			    					for row in result:
			    						stringer += "<br>The topper of "+row[3]+" is "+row[0]+"<br>"
			    			if subflag == 0:
			    				sql = """drop view if exists totals"""
			    				cursor.execute(sql)
			    				sql = "CREATE VIEW totals AS SELECT Name AS totname, Register_number AS totreg, Dept AS totdept,SUM(Marks) AS total FROM student A, mark B where A.Register_number= B.Regno GROUP BY A.Register_number"
			    				cursor.execute(sql)
			    				for dp in deptlister:
			    					dp = dp.upper()
				    				sql = "SELECT totname, totreg, total, totdept FROM totals where total = (SELECT MAX(total) from totals group by totdept having totdept= '%s')" % (dp)
				    				cursor.execute(sql)
				    				result = cursor.fetchall()
				    				for row in result:
				    					stringer += "<br>The topper of "+row[3]+" is "+row[0]+"<br>"
			    			subflag = 0
			    		if reply in ["percentage","percent"]:
			    			subflag = 0
			    			for reply in replierlist:
			    				print(deptlister)
			    				if reply in deptlister:
			    					subflag = 1 
			    					reply = reply.upper()
			    					print(reply)
			    					cursor.execute("delete from passstatus")
			    					cursor.execute("INSERT into passstatus(Regisno,Dpt) SELECT DISTINCT Regno as Regisno,Dept as Dpt from mark")
			    					cursor.execute("drop table if exists pass1")
			    					cursor.execute("drop table if exists total1")
			    					cursor.execute("UPDATE passstatus INNER JOIN mark ON (Regisno = Regno) set Status = 'PASS' where mark.Marks > 49")
			    					cursor.execute("UPDATE passstatus INNER JOIN mark ON (Regisno = Regno)set Status = 'FAIL' where mark.Marks < 50")
			    					cursor.execute("CREATE table pass1 (pass INT,dept VARCHAR(50)) SELECT COUNT(*) as pass, Dpt as dept FROM passstatus WHERE Status = 'PASS' and Dpt = '%s'" %(reply))
			    					cursor.execute("CREATE table total1 (pass INT,dept VARCHAR(50)) SELECT COUNT(*) as pass, Dpt as dept FROM passstatus WHERE Dpt = '%s'" %(reply))
			    					cursor.execute("""SELECT (pass1.pass * 100)/ (total1.pass), pass1.dept FROM pass1, total1 where pass1.dept = total1.dept""")
			    					result = cursor.fetchall()	
			    					for row in result:
			    						stringer += "<br>The department "+ row[1]+" has a pass percentage of "+ str(row[0])+"<br>"
			    			if subflag == 0:
			    				cursor.execute("delete from passstatus")
			    				cursor.execute("INSERT into passstatus(Regisno,Dpt) SELECT DISTINCT Regno as Regisno,Dept as Dpt from mark")
			    				cursor.execute("drop table if exists pass1")
			    				cursor.execute("drop table if exists total1")
			    				cursor.execute("UPDATE passstatus INNER JOIN mark ON (Regisno = Regno) set Status = 'PASS' where mark.Marks > 49")
			    				cursor.execute("UPDATE passstatus INNER JOIN mark ON (Regisno = Regno)set Status = 'FAIL' where mark.Marks < 50")
			    				cursor.execute("CREATE table pass1 (pass INT,dept VARCHAR(50)) SELECT COUNT(*) as pass, Dpt as dept FROM passstatus WHERE Status = 'PASS' GROUP BY Dpt")
			    				cursor.execute("CREATE table total1 (pass INT,dept VARCHAR(50)) SELECT COUNT(*) as pass, Dpt as dept FROM passstatus GROUP BY dept")
			    				cursor.execute("""SELECT (pass1.pass * 100)/ (total1.pass), pass1.dept FROM pass1, total1 where pass1.dept = total1.dept""")
			    				result = cursor.fetchall()	
			    				for row in result:
			    					stringer += "<br>The department "+ row[1]+" has a pass percentage of "+ str(row[0])+"<br>"
			    			subflag = 0
			    if reply in ["subject","subjects"]:
			    	flag = 1
			    	for reply in replierlist:
			    		if reply in ["average","averages"]:
			    			sql = "select Subject, AVG(Marks) from mark group by Subject"
			    			cursor.execute(sql)
			    			result = cursor.fetchall()
			    			for row in result:
			    				stringer += "<br>The average recorded for "+row[0]+" is "+str(row[1])+"<br>"
			    		if reply in ["topper","first","best"]:
			    			subflag = 0
			    			for reply in replierlist:
			    				if reply in sublister:
			    					subflag = 1 
			    					reply = reply.upper()
			    					sql = "SELECT Name, Register_number, Marks from student A, mark B where A.Register_number = B.Regno and B.Subject = '%s' and B.Marks = (select MAX(Marks) from mark group by Subject having Subject= '%s')" % (reply,reply)
			    					cursor.execute(sql)
			    					result = cursor.fetchall()
			    					for row in result:
			    						stringer += "<br>The "+reply+" topper is "+row[0]+" with "+str(row[2])+"<br>"
			    			if subflag == 0:
			    				s = ""
			    				for sb in sublister:
			    					sb = sb.upper()
				    				sql = "SELECT Name, Register_number, Subject, Marks from student A, mark B where A.Register_number = B.Regno and B.Subject = '%s' and B.Marks = (select MAX(Marks) from mark group by Subject having Subject ='%s')" %(sb,sb)
				    				cursor.execute(sql)
				    				result = cursor.fetchall()
				    				for row in result:
				    					s += "<br>The "+row[2]+" topper is "+row[0]+" with "+str(row[3])+"<br>"
				    			stringer += s
			    			subflag = 0
			    		if reply in ["percent","percentage"]:
			    			subflag = 0
			    			for reply in replierlist:
			    				if reply in sublister:
			    					subflag = 1 
			    					reply = reply.upper()
			    					cursor.execute("drop table if exists pass")
			    					cursor.execute("drop table if exists total")
			    					sql = "CREATE table pass (pass INT, sub VARCHAR(50)) SELECT COUNT(*) as pass, Subject as sub FROM mark WHERE Marks > 49 and Subject='%s'" %(reply)
			    					cursor.execute(sql)
			    					sql = "CREATE table total (total INT, sub VARCHAR(50)) SELECT COUNT(*) as total, Subject as sub FROM mark WHERE Subject='%s'" %(reply)
			    					cursor.execute(sql)
			    					sql = """SELECT (pass.pass * 100)/ (total.total), pass.sub FROM pass, total where pass.sub = total.sub"""
			    					cursor.execute(sql)
			    					result= cursor.fetchall()
			    					for row in result:
			    						stringer += "<br> The pass percentage of "+row[1]+" is "+str(row[0])+"<br>"
			    			if subflag == 0:
			    				cursor.execute("drop table if exists pass")
			    				cursor.execute("drop table if exists total")
			    				sql = "CREATE table pass (pass INT, sub VARCHAR(50)) SELECT COUNT(*) as pass, Subject as sub FROM mark WHERE Marks > 49 GROUP BY Subject"
			    				cursor.execute(sql)
			    				sql = "CREATE table total (total INT, sub VARCHAR(50)) SELECT COUNT(*) as total, Subject as sub FROM mark GROUP BY Subject"
			    				cursor.execute(sql)
			    				sql = """SELECT (pass.pass * 100)/ (total.total), pass.sub FROM pass, total where pass.sub = total.sub"""
			    				cursor.execute(sql)
			    				result= cursor.fetchall()
			    				for row in result:
			    					stringer += "<br> The pass percentage of "+row[1]+" is "+str(row[0])+"<br>"
			    			subflag = 0 
			if flag == 0:
				stringer += "I am programmed to reply limited as of now and only certain information can be made visible to public"
			flag = 0
		if reply in ["teacher","teachers","staff"]:
			for reply in replierlist:
				if reply in ["rating","scorecard","points","ratings"]:
					utliflag = 1
					strr = "" 
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
						strr += "<br>"+"Position "+str(i)+": "+row[0]+" ( AISNdb Rating: "+str(row[2])+" )"
					stringer += strr
		if reply in ["student","students"]:
			for reply in replierlist:
				if reply in ["pass","passed","passes"]:
					ultiflag = 1
					stro = ""
					cursor.execute("delete from passstatus")
					cursor.execute("INSERT into passstatus(Regisno,Dpt) SELECT DISTINCT Regno as Regisno,Dept as Dpt from mark")
					sql = "UPDATE passstatus INNER JOIN mark ON (Regisno = Regno) set Status = 'PASS' where mark.Marks > 49"
					cursor.execute(sql)
					sql = "UPDATE passstatus INNER JOIN mark ON (Regisno = Regno)set Status = 'FAIL' where mark.Marks < 50"
					cursor.execute(sql)
					flag = 0
					for reply in replierlist:
						namelister = []
						reglister = []
						cursor.execute("select Name from student")
						result = cursor.fetchall()
						for row in result:
							namelister.append(row[0])
						cursor.execute("select Register_number from student")
						result = cursor.fetchall()
						for row in result:
							reglister.append(str(row[0]))
						if reply in namelister:
							flag = 1
							cursor.execute("select Name, Status from student a, passstatus b where a.Register_number=b.Regisno and a.Name='%s'" %(reply))
							result = cursor.fetchall()
							for rober in result:
								stro += "<br>"+(rober[0]).title()+ " has "+rober[1]+"ED<br>"
						if reply in reglister:
							flag = 1
							cursor.execute("select Regisno, Status from passstatus where Regisno = %d" %(int(reply)))
							result = cursor.fetchall()
							for rober in result:
								stro += "<br>"+str(rober[0])+" has "+rober[1]+"ED<br>"
					if flag == 0:
						sql = "SELECT * FROM passstatus" 
						cursor.execute(sql)
						result = cursor.fetchall()
						for row in result:
							stro += "<br>"+str(row[0])+" has "+row[2]+"ED<br>"
					flag = 0
					stringer += stro
				if reply in ["rating","ranking","rank","ranks"]:
					ultiflag = 1
					saro = ""
					cursor.execute("drop table if exists averagerq")
					cursor.execute("drop table if exists passq")
					cursor.execute("drop table if exists totalq")
					cursor.execute("drop table if exists passerq")
					cursor.execute("drop table if exists subratingtableq")
					sql = "create table averagerq (Nam VARCHAR(20), Reg INT, Dpt VARCHAR(20), Avg INT) select Name as Nam, Regno as Reg, Dept as Dpt, AVG(Marks) as Avg from student a, mark b where a.Register_number = b.Regno group by b.Regno" 
					cursor.execute(sql)
					sql = "CREATE table passq (Reg INT,pass INT) SELECT Regno as Reg,COUNT(*) as pass FROM mark WHERE Marks > 49 group by Regno"
					cursor.execute(sql)
					sql = "CREATE table totalq (Reg INT,total INT) SELECT Regno as Reg,COUNT(*) as total FROM mark group by Regno"
					cursor.execute(sql)
					sql = "CREATE table passerq(Re VARCHAR(50), Passavg INT) SELECT passq.Reg as Re, (passq.pass * 100)/ (totalq.total) as Passavg FROM passq, totalq where passq.Reg = totalq.Reg"
					cursor.execute(sql)
					cursor.execute("create table subratingtableq (Reg VARCHAR(20), Point FLOAT) select passerq.Re as Reg, ((averagerq.Avg + passerq.Passavg)/20) as Point from passerq,averagerq where passerq.Re = averagerq.Reg")
					namelister = []
					reglister = []
					cursor.execute("select Name from student")
					result = cursor.fetchall()
					for row in result:
						namelister.append(row[0])
					cursor.execute("select Register_number from student")
					result = cursor.fetchall()
					for row in result:
						reglister.append(str(row[0]))
					flag = 0
					for reply in replierlist:
						if reply in namelister:
							flag = 1 
							cursor.execute("select Nam, Point from averagerq, subratingtableq where averagerq.Reg=subratingtableq.Reg and averagerq.Nam = '%s'"% (reply))
							result = cursor.fetchall()
							for row in result:
								saro += "<br>"+row[0].title() + " has an AISNdb rating of "+ str(row[1])+"<br>"
						if reply in reglister:
							flag = 1
							cursor.execute("select * from subratingtableq where Reg=%d"%(int(reply)))
							result = cursor.fetchall()
							for row in result:
								saro += str(row[0]) + " has an AISNdb rating of "+ str(row[1])+"<br>"
					if flag == 0:
						cursor.execute("select Nam, Point from averagerq, subratingtableq where averagerq.Reg=subratingtableq.Reg")
						result= cursor.fetchall()
						for row in result:
							saro += row[0]+ " has an AISNdb rating of " +str(row[1])+"<br>"
					flag = 0
					stringer += saro
		if reply in ["questions","question paper","question"]:
			flag = 0
			for reply in replierlist:
				if reply in ["easy","easier","easiest","simple","low"]:
					flag = 1
					ultiflag = 1
					with open('question_paper.txt', 'r+') as content_file:
						content = content_file.read()
					strunger = re.split("\d+[)] ",content)
					del strunger[len(strunger) - 1]
					del strunger[0]
					substringer = strunger[0:10]
					print("The easy questions")
					random.shuffle(substringer)
					q1,q2,q3,q4,q5 = substringer[:5]
					print("1. "+q1)
					print("2. "+q2)
					print("3. "+q3)
					print("4. "+q4)
					print("5. "+q5)
					stringer += "<br>The easy questions:</br>"+"1. "+q1+"<br>2. "+q2+"<br>3. "+q3+"<br>4. "+q4+"<br>5. "+q5+"<br>"
				if reply in ["medium","moderate","ok","middle"]:
					flag = 1 
					ultiflag = 1
					with open('question_paper.txt', 'r+') as content_file:
						content = content_file.read()
					strunger = re.split("\d+[)] ",content)
					del strunger[len(strunger) - 1]
					del strunger[0]
					substringer = strunger[6:16]
					print("The moderate questions")
					random.shuffle(substringer)
					q1,q2,q3,q4,q5 = substringer[:5]
					print("1. "+q1)
					print("2. "+q2)
					print("3. "+q3)
					print("4. "+q4)
					print("5. "+q5)
					stringer += "<br>The moderate questions:</br>"+"1. "+q1+"<br>2. "+q2+"<br>3. "+q3+"<br>4. "+q4+"<br>5. "+q5+"<br>"
				if reply in ["hard","difficult","high","tough"]:
					flag = 1 
					ultiflag = 1
					with open('question_paper.txt', 'r+') as content_file:
						content = content_file.read()
					strunger = re.split("\d+[)] ",content)
					del strunger[len(strunger) - 1]
					del strunger[0]
					substringer = strunger[10:20]
					print("The moderate questions")
					random.shuffle(substringer)
					q1,q2,q3,q4,q5 = substringer[:5]
					print("1. "+q1)
					print("2. "+q2)
					print("3. "+q3)
					print("4. "+q4)
					print("5. "+q5)
					stringer += "<br>The tough questions:</br>"+"1. "+q1+"<br>2. "+q2+"<br>3. "+q3+"<br>4. "+q4+"<br>5. "+q5+"<br>"
			if flag == 0:
				ultiflag =1 
				stringer += "<br> May I know the difficulty level thalaiva :P"
			flag = 0
		if reply in ["time table","schedule","plan","timetable"]:
			flag = 0
			deptlister = []
			cursor.execute("select distinct Dept from mark")
			result = cursor.fetchall()
			for row in result:
				deptlister.append(row[0].lower())
			for reply in replierlist:
				ding = ""
				if reply in deptlister:
					ding = ""
					flag = 1
					ultiflag = 1
					sublister = []
					pointlister = []
					dailylist = []
					reply = reply.upper()
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
					sql = "select distinct Sub,Point from subratingtable a,mark b where a.Sub = b.Subject and b.Dept ='%s'" % (reply)
					cursor.execute(sql)
					result = cursor.fetchall()
					stringer += "<div class=""table-responsive""><table class=""table table-hover""><thead><tr><th>DAYS/PERIODS</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th></tr></thead><tbody>"
					for x in result:
						sublister.append(x[0])
					for y in result:
						pointlister.append(y[1])
					periods = 8
					for i in range(0, len(pointlister)):
						if pointlister[i]> 8:
							count = periods * 0.2
							while(count>0):
								dailylist.append(sublister[i])
								count -= 1
						elif pointlister[i]>= 6 and pointlister[i]<=8:
							count = periods * 0.3
							while(count>0):
								dailylist.append(sublister[i])
								count -= 1
						else:
							count = periods * 0.5
							while(count>0):
								dailylist.append(sublister[i])
								count -= 1
					days = 6
					aliasdays = days 
					while(days>0):
						random.shuffle(dailylist)
						ding+="<tr>"
						ding += "<td>"+str(aliasdays - days + 1)+"</td>"
						for x in range(0,periods):
							ding += "<td>"+str(dailylist[x])+"</td>"
						days -= 1 
						ding += "</tr>"
					ding += "</tbody></table></div><hr>"
				stringer += ding
			if flag == 0:
				ultiflag = 1
				stringer += "<br> Can you be specific with the department sir<br>"
			flag =0
	if ultiflag == 0:
		stringer += "<br> I am not programmed to answer those<br>"
	ultiflag = 0
	return """<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">"""+"""<style> a:link, a:visited {
    padding: 14px 25px;
    text-align: center;	
    text-decoration: none;
    display: inline-block;
}


a:hover, a:active {
   text-decoration: none;
   color: hotpink;
}
</style>"""+"""<div class="container">"""+"""<div class = "page-header">"""+"<h1>AISN RESPONSE</h1>"+"</div>"+"""<div class= "jumbotron">"""+"""<p class="text-center">"""+stringer+"<a href='/speak'> Go back to AISN </a></p>"+"</div>"+"</div>"
if __name__ == "__main__":
	app.debug = True
	app.run(host="localhost")

