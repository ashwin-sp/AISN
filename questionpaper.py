import random
import re

with open('question_paper.txt', 'r+') as content_file:
    content = content_file.read()

stringer = re.split("\d+[)] ",content)
del stringer[len(stringer) - 1]
del stringer[0]

choice= input("'Easy' or 'medium' or 'tough' question paper??").lower()
if(choice == "easy"):
	substringer = stringer[0:10]
	print("The easy questions")
	random.shuffle(substringer)
	q1,q2,q3,q4,q5 = substringer[:5]
	print("1. "+q1)
	print("2. "+q2)
	print("3. "+q3)
	print("4. "+q4)
	print("5. "+q5)
elif(choice == "medium"):
	substringer = stringer[6:16]
	print("The moderate questions")
	random.shuffle(substringer)
	q1,q2,q3,q4,q5 = substringer[:5]
	print("1. "+q1)
	print("2. "+q2)
	print("3. "+q3)
	print("4. "+q4)
	print("5. "+q5)
else:
	substringer = stringer[10:20]
	print("The tough questions")
	random.shuffle(substringer)
	q1,q2,q3,q4,q5 = substringer[:5]
	print("1. "+q1)
	print("2. "+q2)
	print("3. "+q3)
	print("4. "+q4)
	print("5. "+q5)