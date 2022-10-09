from kafka import KafkaProducer
from datetime import datetime
import os
import time
import random
import sys
import config as cfg
import json

data_dir = '../data'
# import logging
# logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    print("Kafka Producer Application Started ... ")

    kafka_producer_obj = None
    kafka_producer_obj = KafkaProducer(bootstrap_servers=cfg.BOOTSTRAP_SERVERS_CONS,
                                       api_version=(0, 10, 1),
                                       value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    data = json.load(open(os.path.join(data_dir, 'test.json')))
    try:
        for idx, (k, v) in enumerate(data.items()):
            event_message = {}
            event_datetime = datetime.now()
            
            event_message['event_datetime'] = str(event_datetime)
            event_message['event_context'] = v['context']
            event_message['event_sentences'] = ''.join(v['turns'])
            # event_message['sentence_id'] = int(k)
            # event_message['event_id'] = idx

            print(f"Printing message id: {idx}")
            kafka_producer_obj.send(cfg.TOPIC_NAME_CONS, event_message)
            time.sleep(0.05)
            if idx == 10:
                break

    except Exception as e:
        print("Event Message Construction Failed. ")
        print(e)
        sys.exit()

    print("Kafka Producer Application Completed. ")
