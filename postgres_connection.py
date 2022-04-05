
import psycopg2
from config import config
import json

def insert_history_data(data):   
    data = json.loads(data)
    print("connected postgres")
    params = config()
    connection = psycopg2.connect(**params)
    print("connected postgres")
    crsr = connection.cursor()
    query = " insert into history ( event, messageid, userid, properties, context,clicked_date ) values (%s,%s,%s,%s,%s,%s)"
    record_to_insert = (data['event'], data['messageId'], data['userId'], data['properties']['productid'],data['context']['source'],data['datettime'])
    crsr.execute(query,record_to_insert)
    connection.commit() 


def get_data_by_userid(user_id):
    params = config()
    connection = psycopg2.connect(**params)
    crsr = connection.cursor()
    query = " select id, o.product_id, o.quantity, o.order_id, r.user_id, p.category_id from order_items o inner join orders r on o.order_id = r.order_id  inner join products p on o.product_id = p.product_id where user_id ="+ "'" + user_id + "'"
    crsr.execute(query)
    result = crsr.fetchall()        
    return result


def get_history_by_userid(user_id):
    params = config()
    connection = psycopg2.connect(**params)
    crsr = connection.cursor()
    query = " select properties from history where userid ="+ "'" + user_id + "' order by clicked_date desc limit 10"
    crsr.execute(query)
    data = crsr.fetchall()        
    result = []
    for i in data:
        result.extend(i)
    res = {"user-id":user_id,"products":result,"type":'personalized'}
    return res


def delete_user_history_byId(user_id,product_id):
    params = config()
    connection = psycopg2.connect(**params)
    crsr = connection.cursor()
    query = " delete from history where userid ="+ "'" + user_id + "' and properties =" +  "'" + product_id + "'"
    crsr.execute(query)
    connection.commit() 

def get_recommodations(user_id):
    params = config()
    print("1")
    connection = psycopg2.connect(**params)
    print("2")
    crsr = connection.cursor()
    print("3")
    query = " select distinct p.category_id, count(h.properties) products_count   from history h inner join products p on h.properties = p.product_id where h.userid= "+  "'" + user_id + "'" + " group by p.category_id order by products_count desc limit 3"
    print("4")
    crsr.execute(query)
    print("5")

    categories = crsr.fetchall()
    print("categories",categories)
    result = []
    if categories:
        for category in categories:
            res = get_products_by_category_id(category[0])
            result.extend(res)
        res = {"user-id":user_id,"products":result,"type":'non-personalized'}
        return res
    else:
        return result

def get_products_by_category_id(category_id):
    params = config()
    connection = psycopg2.connect(**params)
    crsr = connection.cursor()
    query = "select o.product_id, p.category_id from order_items o inner join products p on o.product_id = p.product_id where p.category_id = "+  "'" + category_id + "'" + " group by o.product_id,o.quantity,p.category_id order by quantity desc limit 10;"
    crsr.execute(query)
    products = crsr.fetchall()
    print(products)
    return products