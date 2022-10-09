import config as cfg
from json import loads
from pyspark.sql import SparkSession, HiveContext, Row
from kafka import KafkaConsumer
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.ml import Pipeline
from pyspark.sql.functions import array_contains
from pyspark.ml import Pipeline, PipelineModel

import sparknlp
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline

sparknlp = sparknlp.start()
# pipeline = PretrainedPipeline("analyze_sentiment", lang="en")

import json
import os
import sys

# os.environ['PYSPARK_PYTHON'] = 'python3.9.13'
# os.environ['PYSPARK_DRIVER_PYTHON'] = 'C:/Users/PAC/miniconda3/envs/spark3.9/python.exe'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.2.5 pyspark-shell'
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars file:///C:/apache_spark/spark_dependency/postgresql-42.2.5.jar pyspark-shell'

spark = SparkSession.builder \
     .master('spark://spark-master:7077') \
     .config('spark.jars.packages', 'C:/apache_spark/spark_dependency/postgresql-42.2.5.jar') \
     .appName('test spark pipeline') \
     .enableHiveSupport() \
     .getOrCreate()

df = spark.read \
          .format("jdbc") \
          .option("url", "jdbc:postgresql://hive-metastore-postgresql:5432/postgres_test") \
          .option("driver", "org.postgresql.Driver") \
          .option("dbtable", "dbtable_test") \
          .option("user", "user") \
          .option("password", "admin") \
          .load()

print(df)
sys.exit()

# spark = SparkSession.builder \
#      .master('spark://spark-master:7077') \
#      .config('spark.jars', 'C:/apache_spark/spark_dependency/postgresql-42.2.16.jar') \
#      .config("spark.executor.extraClassPath",'C:/apache_spark/spark_dependency/postgresql-42.2.16.jar') \
#      .appName('test spark pipeline') \
#      .enableHiveSupport() \
#      .getOrCreate()

# spark.conf.set('fs.defaultFS', 'hdfs://datanode:50010')

schema = StructType([StructField('datetime',StringType(),True),
                     StructField('server_type',StringType(),True),])
                    #  StructField('event_sentences',StringType(),True),])

if __name__ == '__main__':
    print('Application Started ...')
    try:

        


        consumer = KafkaConsumer(cfg.TOPIC_NAME_CONS,
                                 bootstrap_servers=cfg.BOOTSTRAP_SERVERS_CONS,
                                 auto_offset_reset='latest', # or earliest
                                 enable_auto_commit=True,
                                 group_id=cfg.KAFKA_CONSUMER_GROUP_NAME_CONS,
                                 value_deserializer=lambda x: loads(x.decode('utf-8')))
        for idx, d in enumerate(consumer):
            
            data = [(d.value['event_datetime'], d.value['event_context'])]
            # , d.value['event_sentences'])]
            df = spark.createDataFrame(data=data,schema=schema)
            print(df.show())
            print(df.printSchema())

            # df.coalesce(1).write.format('json').save('hdfs://172.18.0.9:50010/test')
            # df.write.csv(f'df_{idx}.csv')
            # df.write.format('csv').option('header',True).save(f'hdfs://172.18.0.9:50010/test_{idx}.csv')
            # df.write.option("header","true").csv("hdfs://datanode:50075/csvfile.csv")
            # df.write.json("hdfs://namenode:50010/jsonfile")
            # df.rdd.saveAsTextFile("json") 

            # result = pipeline.annotate(d.value['context'])
            # print(result['sentiment'])
            # result = pipeline.annotate(d.value['sentences'])
            # print(result['sentiment'])
            # print('######')

            # df.repartition(1).write.option("header", "true").format("csv").save(path)

            df.select('datetime','server_type').write.format('jdbc')\
              .option('url', 'jdbc:postgresql://hive-metastore-postgresql:5432/postgres_test') \
              .option('driver', 'org.postgresql.Driver') \
              .option('dbtable', 'dbtable_test') \
              .option('user', 'user') \
              .option('password', 'admin') \
              .save()

            # db_properties = {'user': 'user', 
            #                  'password': 'admin',
            #                  'driver': 'org.postgresql.Driver'}

            # df.write.jdbc(url = 'jdbc:postgresql://hive-metastore-postgresql:5432/postgres',
            #               table = 'dbtable',
            #               mode = 'append',
            #               properties = db_properties)

        print('finished')
    except Exception as e:
        print('Failed to read kafka message.')
        print(e)