lines = sc.textFile("/Users/raphaeluzan/Desktop/mapreduce/data.txt")
lines = lines.map(lambda x : (x.split('\t')[0],x.split('\t')[1].split()))
lines.reduceByKey(lambda x,y: x+y).collect()
lines = lines.rdd.map(lambda x : (x.split('\t')[0],x.split('\t')[1]))

def f(x): 
	return x


def get_res(x,y):
	if x=="B" or y =="B" :
		return False
	else:
		return True

def replacee(var):
	if var == "B":
		return False
	elif var == "A":
		return True
	else :
		return var

lines = lines.flatMapValues(f).map(lambda x : (x[1],x[0])).reduceByKey(lambda x,y : get_res(x,y) )
lines.collect()


lines.map(lambda x : (x[0],replacee(x[1]))).collect()
