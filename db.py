import pymysql
from flask import jsonify
from uuid import uuid4

def uuid_hex():
	return uuid4().hex

def query(querystr,return_json=True):
    connection=pymysql.connect( host='skillup.cxgok3weok8n.ap-south-1.rds.amazonaws.com',
                                user='admin',
                                password='Pinky123',
                                db='yorking',
                                cursorclass=pymysql.cursors.DictCursor )
    connection.begin()
    cursor=connection.cursor()
    cursor.execute(querystr)
    result=cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    if return_json: return jsonify(result)
    return result
