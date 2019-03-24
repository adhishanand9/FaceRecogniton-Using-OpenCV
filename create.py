#!/usr/bin/python

import psycopg2
from datetime import date

today = str(date.today())
# print(today)

conn = psycopg2.connect(database = "testdb2", user = "postgresql", password = "namespace1", host = "sample-database.czgprnseypbr.us-east-1.rds.amazonaws.com", port = "5432")
print ('Opened database successfully')
cur = conn.cursor()

students = 5

str1 = "CREATE TABLE MAINATT (ROLL int,\""
str1 +=today
str1 += "\" int);"
cur.execute(str1)
print("Created successfully mainatt")

str1 = "CREATE TABLE second (ROLL int,Attended int,total int);"
cur.execute(str1)
print("Created successfully second")


# now inserting in table
for student in range(1,students+1):
    str1 = "INSERT INTO MAINATT (ROLL,\""
    str1 += today
    str1 += "\") VALUES ("
    str1 += str(student)
    str1 += ",0);"
    # print(str1)
    cur.execute(str1)

    str1 = "INSERT INTO SECOND (ROLL,ATTENDED,TOTAL) VALUES ("
    str1+=str(student)
    str1+=",0,1);"
    cur.execute(str1)
print("Data inserted successfully")
conn.commit()
conn.close()