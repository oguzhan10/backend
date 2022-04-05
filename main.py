from fastapi import FastAPI
import uvicorn
from kafka_connection import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    r'http://0.0.0.0:3000',
    r'http://172.17.240.1:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(r'/')
def send_welcome():
    return "challenge"


@app.get(r'/send_to_kafka')
def send_to_kafka():
    try:
        send_data_to_kafka()
    except AssertionError as error:
        return error

@app.get(r'/run_kafka_consumer')
def run_kafka_consumer():
    try:
        consume_from_kafka()    
    except AssertionError as error:
        return error

@app.get(r'/user_history/{user_id}')
def user_history(user_id:str):
    try:
        result = get_history_by_userid(user_id)
        return result
    except AssertionError as error:
        return error

@app.get(r'/recommendation_by_user_id/{user_id}')
def recommendation_by_user_id(user_id:str):
    try:
        res = get_recommodations(user_id)
        return res
    except AssertionError as error:
        return error

@app.delete(r'/delete_user_history_by_product_id/{user_id}/{product_id}')
def delete_user_history_by_product_id(user_id:str,product_id:str):
    try:
        delete_user_history_byId(user_id,product_id)
        return "success"
    except AssertionError as error:
        return error
 