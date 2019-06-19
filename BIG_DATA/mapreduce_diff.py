'''
# commande :
cat data.txt | python mapper.py | sort -k1,1 | python reducer.py


# data.txt
A       toto tata tete tutu
A       toto tota tyty
B       titi
A       titi toto
B       tato
'''

# mapper.py
import sys

for line in sys.stdin:
	line = line.strip()
	words = line.split('\t')
	type_ligne = words[0]
	datas = words[1].split(' ')
	for data in datas:
		print(type_ligne + '\t' + data)


# reducer.py
import sys

def take_value(key,res_a,res_b):
	if key in res_a :
		return True 
	else:
		return False

def set_value(typee,value):
	if value in res:
		if typee ==  "B":
			return False
		else:
			return res[value]
	else:
		if typee == "A":
			return True
		elif typee == "B":
			return False


res = {}

for line in sys.stdin:
	line = line.strip()
	data = line.split('\t')
	res[data[1]] = set_value(data[0],data[1])

for i in res.keys():
	if res[i]:
		print(i)
 
