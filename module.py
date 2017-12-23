import getpass
from nltk import wordpunct_tokenize

user = "root"
password = "root"
stringer = ""

userInput = str(input("Enter the user name and password"))
passInput = str(getpass.getpass())

if(userInput == "root" and passInput == "root"):
	stringer =str(input("Hello master, Do you want to insert/update/delete/view students or teachers or marks or do you want to know their performance?"))
	stringer = stringer.lower()
	reply = list(set(wordpunct_tokenize(stringer)))
	print(reply)
	flag = 0
	for r in reply:
		if r in ["student","students"]:
			flag = 1
			import studentdb
		if r in ["teacher","teachers","faculty","staff"]:
			flag = 1
			import teacherdb
		if r in ["mark","marks","grades"]:
			flag = 1 
			import markdb
		if r in ["performance","results","result","question","paper","salary"]:
			flag = 1 
			import perfomancedb
	if flag == 0:
		print("I can't get you master please try to speak in an understandable langauge or contact admin for not training me to understand you")
else:
	print("Invalid user name or password")



