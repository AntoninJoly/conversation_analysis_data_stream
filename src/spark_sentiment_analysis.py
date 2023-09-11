import json
import os
import sys
import sys
sys.path.append('../')
import config as cfg
from starlette.config import Config
cfg_pg = Config('../.env')

# import pyspark
# from pyspark import SparkConf

from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline

from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, udf, col, lit
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, IntegerType

# from sqlalchemy import create_engine

# Set up necessary environment variables for Spark
# os.environ["PYSPARK_SUBMIT_ARGS"] = ("--packages com.johnsnowlabs.nlp:spark-nlp_2.12:5.1.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3,org.json4s:json4s-jackson_2.12:3.6.7 pyspark-shell")

def write_to_postgres(df, epoch_id):

    url = f'jdbc:postgresql://localhost:5432/{cfg.POSTGRES_DB_NAME}'
    username = cfg_pg('pg_username')
    pw = cfg_pg('pg_pw')

    df.write.format('jdbc')\
            .option('url', url).option('dbtable', 'conversation_summary')\
            .option('user', username).option('password', pw)\
            .option('driver', 'org.postgresql.Driver')\
            .mode('append').save()
    
# # Start Spark Session
# spark = sparknlp.start()


if __name__ == '__main__':
    print('Application Started ...')
    # .config('spark.jars.packages', 'org.apache.spark:spark-streaming-kafka-0-10_2.12:3.1.2') \
    # .config("spark.driver.memory", "16G") \
    # .config("spark.driver.maxResultSize", "0") \
    # .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    # .config("spark.kryoserializer.buffer.max", "2000m") \
    # .config("spark.jsl.settings.pretrained.cache_folder", "sample_data/pretrained") \
    # .config("spark.jsl.settings.storage.cluster_tmp_dir", "sample_data/storage") \
    # .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:5.1.0") \
    # .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2') \

    spark = SparkSession.builder \
                        .appName('SparkNLP on Kafka Stream') \
                        .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:5.1.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
                        .getOrCreate()
    print('Connected to Spark')

    # Read the data from kafka
    streaming_df = spark.readStream.format('kafka') \
                        .option('kafka.bootstrap.servers', 'localhost:9093') \
                        .option('subscribe', cfg.TOPIC_NAME_CONS) \
                        .option('startingOffsets', 'latest') \
                        .option('header', 'true') \
                        .load()
    deserializedDF = streaming_df.selectExpr('CAST(value AS STRING) as value')
    jsonDF = deserializedDF.selectExpr("json_tuple(value, 'user_name', 'sentence_id', 'event_context')")\
                           .toDF(*['user_name', 'sentence_id', 'event_context'])
    
    # # Process data
    # schema = StructType([StructField('user_name', StringType(),True),
    #                      StructField('sentence_id', StringType(),True),
    #                      StructField('event_context', StringType(),True)])
    # df = streaming_df.withColumn('json', from_json(col('value'), schema))
    # df = df.select('json.user_name','json.sentence_id','json.event_context')

    df_spark = jsonDF.withColumn('label', lit('neutral'))
    df_spark = df_spark.withColumn('user_name', lit(10))
    df_spark = df_spark.toDF(*['user_id', 'conversation_id', 'summarized_msg', 'label'])
    data  = df_spark.select('summarized_msg').toDF('text')

    pipeline = PretrainedPipeline('analyze_sentiment', lang='en')
    pred = pipeline.transform(data)
    # c = os.getcwd()
    # pred.writeStream.outputMode("append").format('csv').option("checkpointLocation", os.path.join(c, "checkpoint")).option("path", c).start().awaitTermination()
    pred.writeStream.format('console').option("truncate", "false").start().awaitTermination()


    # query = df_spark.writeStream.outputMode('append').foreachBatch(write_to_postgres).start()
    # query.awaitTermination()
    # url = f'jdbc:postgresql://localhost:5432/{cfg.POSTGRES_DB_NAME}'
    # username = cfg_pg('pg_username')
    # pw = cfg_pg('pg_pw')
    
    # query = df.writeStream.format('jdbc').option('driver', 'org.postgresql.Driver') \
    #                       .option('url', url).option('dbtable', 'conversation_summary') \
    #                       .option('user', username).option('password', pw) \
    #                       .start()
    # query.awaitTermination()

    # # mode = 'overwrite'
    # url = f'jdbc:postgresql://localhost:5432/{cfg.POSTGRES_DB_NAME}'
    # properties = {'user':username, 'password':pw, 'driver': 'org.postgresql.Driver'}
    # df.writeStream.jdbc(url=url, table='conversation_summary', properties=properties)
    # df.write.jdbc(url=url, table='conversation_summary', mode=mode, properties=properties)
    # df.write.option('driver', 'org.postgresql.Driver').jdbc(url, 'conversation_summary', mode, properties)