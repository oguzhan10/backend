import json
import pandas as pd
import datetime
from kafka import KafkaProducer
from kafka import KafkaConsumer
from postgres_connection import *
import time

IP = "127.0.0.1:9092"
TOPIC = 'history'

def send_data_to_kafka():
    obj =datetime.datetime.now()
    producer = KafkaProducer(bootstrap_servers=[IP],                        
                        value_serializer=lambda x: 
                        json.dumps(x).encode('utf-8'))
    productViews = pd.read_json('product-views.json', lines=True, orient='records')        
    ordersDataFrame = pd.DataFrame(productViews)
    for index,line in ordersDataFrame.iterrows():
        _date = obj + datetime.timedelta(days=1*index,hours=1*index)
        data = {'event':line['event'],'messageId':line['messageid'],'userId':line['userid'],
        'properties':line['properties'],'context':line['context'],'datettime':datetime.datetime.strftime(_date,"%m/%d/%Y %H:%M:%S")}
        producer.send(TOPIC, value=data)
        time.sleep(1)
    return 'success'

def consume_from_kafka():
    print("consume_from_kafka")
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[IP],
        group_id='my-group')
    for message in consumer:
        insert_history_data(message.value)    
    KafkaConsumer.close()
    return 'success'

