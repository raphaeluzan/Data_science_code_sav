
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
from pyspark.sql.types import StringType



# Create spark session
spark = SparkSession.builder.master("local").appName("iris").getOrCreate()

# build the scema to load the dataframe. 
colnames = ["user", "item", "rating", "timestamp" ]
a = [ StructField(colname, FloatType(), False) for colname in colnames ]

schema = StructType (a)

# assembler group all x1..x2 into a single col called X
assembler = VectorAssembler( inputCols = colnames[:-1], outputCol="features" )


training.select("user").distinct().count()
training.select("item").distinct().count()
## TRAINING 

# load the data into the dataframe
training = spark.read.csv("hdfs:///user/user58/data/movielens10M.train", schema = schema)

from pyspark.ml.recommendation import ALS
als = ALS(rank=10, maxIter=5, seed=0)
model = als.fit(training)
model.rank

pred = model.transform(training)


from pyspark.sql.functions import col
from pyspark.sql.functions import udf
import pyspark.sql.functions as F

def f(rating,prediction):
	return (float(rating)-float(prediction))* (float(rating)-float(prediction))


udf_day = udf(f, FloatType())

err = pred.withColumn("error", udf_day(pred["rating"],pred["prediction"]))

#err.show()

n= training.select("user").distinct().count()




import math
rmse = math.sqrt(err[["error"]].groupBy().sum().collect()[0][0]/n)
