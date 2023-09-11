import json
import os
import sys
import config as cfg
from pymongo import MongoClient

from kafka import KafkaConsumer

if __name__ == '__main__':
    print('Application Started ...')
    try:
        client = MongoClient('localhost', 27017)
        db = client.datalake_stream_msg
        print("Connected successfully to mongoDB!")
    except:  
        print("Could not connect to MongoDB")

    try:
        consumer = KafkaConsumer(cfg.TOPIC_NAME_CONS,
                                bootstrap_servers=cfg.BOOTSTRAP_SERVERS_CONS,
                                auto_offset_reset='latest', # or earliest
                                enable_auto_commit=True,
                                group_id=cfg.KAFKA_CONSUMER_GROUP_NAME_CONS,
                                value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        print("Connected successfully to kafka consumer!")
    except:
        print('Cannot connect to kafka producer')

    for idx, msg in enumerate(consumer):
        try:
            rec = {'timestamp':msg.value['event_datetime'],
                   'message':msg.value['event_context'],
                   'user_name':msg.value['user_name']}
            rec_id = db.stream_messages.insert_one(rec)
            print("Data inserted with record ids", rec_id)
        except:
            print("Could not insert into MongoDB")
