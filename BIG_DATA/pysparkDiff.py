
# fonction utile
def f(x): 
	return x

# gérer la fusion des values dans le reduce by key
def get_res(x,y):
	if x=="B" or y =="B" :
		return False
	else:
		return True

#le reduceByKey ne transforme pas les élément unique d'une key, on les gere donc grace a cette fonction
def replacee(var):
	if var == "B":
		return False
	elif var == "A":
		return True
	else :
		return var
	
	
	
lines = sc.textFile("/Users/raphaeluzan/Desktop/mapreduce/data.txt") # load les données en rdd
lines = lines.map(lambda x : (x.split('\t')[0],x.split('\t')[1].split())) #on split le type avec les lignes elles memes
lines = lines.flatMapValues(f).map(lambda x : (x[1],x[0])).reduceByKey(lambda x,y : get_res(x,y) ) # on flatmap les values et 
#on inverse les Key avec les values pour pouvoir fusionner par mot en fonction du texte auxquel il appartient

lines.map(lambda x : (x[0],replacee(x[1]))).collect()#on gere les clé avec une unique value que le reduceByKey a ignore


