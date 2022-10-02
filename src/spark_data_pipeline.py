# import sched
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
pipeline = PretrainedPipeline("analyze_sentiment", lang="en")

import json
import os
import sys

spark = SparkSession.builder \
     .master('spark://spark-master:7077') \
     .config('spark.jars', 'C:/apache_spark/spark_dependency/postgresql-42.2.16.jar') \
     .appName('test spark pipeline') \
     .enableHiveSupport() \
     .getOrCreate()

spark.conf.set('fs.defaultFS', 'hdfs://192.168.0.2:50010')

schema = StructType([StructField('datetime',StringType(),True),
                     StructField('context',StringType(),True),
                     StructField('sentences',StringType(),True),])

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
            
            data = [(d.value['datetime'], d.value['context'], d.value['sentences'])]
            df = spark.createDataFrame(data=data,schema=schema)
            # df.write.csv(f'df_{idx}.csv')
            df.write.format('csv').option('header',True).mode('overwrite').option('sep','|').save('/output.csv')
            
            result = pipeline.annotate(d.value['context'])
            print(result['sentiment'])
            result = pipeline.annotate(d.value['sentences'])
            print(result['sentiment'])
            print('######')

            # df.repartition(1).write.option("header", "true").format("csv").save(path)
            # try:
            #     sc_uri = spark.sparkContext._gateway.jvm.java.net.URI
            #     sc_path = spark.sparkContext._gateway.jvm.org.apache.hadoop.fs.Path
            #     file_system = spark.sparkContextc._gateway.jvm.org.apache.hadoop.fs.FileSystem
            #     configuration = spark.sparkContext._gateway.jvm.org.apache.hadoop.conf.Configuration
                
            #     fs = file_system.get(sc_uri("hdfs://{HDFS_IP/NAME}"), configuration())
            #     src_path = None
            #     status = fs.listStatus(sc_path(path))
                
            #     for fileStatus in status:
            #         temp = fileStatus.getPath().toString()
            #         if "part" in temp:
            #             src_path = sc_path(temp)
                
            #     dest_path = sc_path(path + filename)
            #     if fs.exists(src_path) and fs.isFile(src_path):
            #         fs.rename(src_path, dest_path)
            #         fs.delete(src_path, True)
            # except Exception as e:
            #     raise Exception("Error renaming the part file to {}:".format(filename, e))


            # df.select('datetime','server_type').write.format('jdbc')\
            #   .option('url', 'jdbc:postgresql://localhost:5432/postgres') \
            #   .option('driver', 'org.postgresql.Driver') \
            #   .option('dbtable', 'test_df') \
            #   .option('user', 'user') \
            #   .option('password', 'admin') \
            #   .save()

            # db_properties = {'user': 'user', 
            #                  'password': 'admin',
            #                  'driver': 'org.postgresql.Driver'}

            # df.write.jdbc(url = 'jdbc:postgresql://127.0.0.1:6543/postgres',
            #               table = 'dbtable',
            #               mode = 'append',
            #               properties = db_properties)

        print('finished')
    except Exception as e:
        print('Failed to read kafka message.')
        print(e)