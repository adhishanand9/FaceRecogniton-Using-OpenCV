#!/usr/bin/env python
from flask import Flask, jsonify, request
app = Flask(__name__)

import psycopg2
import threading
import time

conn = psycopg2.connect(database = "testdb2", user = "postgresql", password = "namespace1", host = "sample-database.czgprnseypbr.us-east-1.rds.amazonaws.com", port = "5432")
print ('Opened database successfully')
cur = conn.cursor()

        



@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works'})

@app.route('/getattendence', methods=['GET'])
def ow():
    global cur
    cur.execute("SELECT * from SECOND")
    rows = cur.fetchall()
    data = []
    for row in rows:
        print(row)
        roll = str(row[0])
        attended = str(row[1])
        total = str(row[2])
        data += [{'roll':roll,'attended':attended,'total':total}]
    return jsonify(data)
dt = []
@app.route('/getattendence/<string:condition>', methods=['GET'])
def ow2(condition):
    global cur
    cur.execute("SELECT * from SECOND")
    rows = cur.fetchall()
    data = []
    for row in rows:
        if(str(row[0]) == str(condition)):
            roll = str(row[0])
            attended = str(row[1])
            total = str(row[2])
            data += [{'roll':roll,'attended':attended,'total':total}]
        else:
             print(type(row[0]))
             print(type(condition))
    #     data += [{'roll':roll,'attended':attended,'total':total}]
    # langs = [dt for dt in data if data[0] == int(nameq) ]
    return jsonify(data)






# if __name__ == '__main__':
#     app.run(debug=True)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")




