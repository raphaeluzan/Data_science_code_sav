from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import VectorAssembler

from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import FloatType

# Create spark session
spark = SparkSession.builder.master("local").appName("iris").getOrCreate()

# build the scema to load the dataframe. 
colnames = ["x1", "x2", "x3", "x4", "y" ]
schema = StructType ( [ StructField(colname, FloatType(), False) for colname in colnames ] )
# assembler group all x1..x2 into a single col called X
assembler = VectorAssembler( inputCols = colnames[:-1], outputCol="X" )

## TRAINING 

# load the data into the dataframe
training = spark.read.csv("iris_bin.train", schema = schema)
training = assembler.transform(training) #group all x1..x2 into a single col called X

# keep X and y only
training = training.select("X", "y")

print("Schema: ")
training.printSchema()

print("Data")
print(training.show())


lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8, labelCol="y",featuresCol="X")
lrModel = lr.fit(training)


print("-----------------------------------------------------")

testing = spark.read.csv("iris_bin.test", schema = schema)
testing = assembler.transform(testing) #group all x1..x2 into a single col called X

# keep X only
testing = testing.select("X")

print("Schema: ")
testing.printSchema()

print("Data")
print(testing.show())


print("-----------------------------------------------------")

#Predictions

predictions = lrModel.transform(testing)
predictions.show()


#acc = predictions.filter(prediction.y == prediction.prediction).count() Compte le nombre de predictions correct (compare les predictions et les vrais étiquettes)

