import MySQLdb
import random

sql = ""
db = MySQLdb.connect("localhost", "root", "root", "ashwin")
cursor = db.cursor()
dept=input("Enter the department for which you need to frame a time-table")
days = int(input("Enter the number of days of the week"))
periods = int(input("Enter the number of periods for the day"))

sublister = []
pointlister = []
dailylist = []
sql = "select distinct Sub,Point from subratingtable a,mark b where a.Sub = b.Subject and b.Dept ='%s'"%(dept)
cursor.execute(sql)
result = cursor.fetchall()
for x in result:
	sublister.append(x[0])

for y in result:
	pointlister.append(y[1])

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
aliasdays = days
while(days>0):
	random.shuffle(dailylist)
	print("Day:%d" %(aliasdays - days + 1), end = ' ')
	for x in range(0,periods):
		print(dailylist[x],end = ' ')
	days -= 1
	print(end='\n')
