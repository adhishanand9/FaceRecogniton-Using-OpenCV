#!/usr/bin/python

import psycopg2
from datetime import date
conn = psycopg2.connect(database = "testdb2", user = "postgresql", password = "namespace1", host = "sample-database.czgprnseypbr.us-east-1.rds.amazonaws.com", port = "5432")
print ('Opened database successfully')
cur = conn.cursor()

def upload(rollno):
    today = str(date.today())
    # print(today)


    students = 5

    # today = "2019-03-29"
    # rollno = 3  

    str1 = "SELECT column_name FROM information_schema.columns where table_name='mainatt' and column_name='"
    str1 += today
    str1 +="';"
    cur.execute(str1)
    rows = cur.fetchall()
    print(rows)
    if(rows):
        str3 = "SELECT \""
        str3 += today
        str3 += "\" FROM MAINATT WHERE ROLL="
        str3 += str(rollno)
        str3 += ";"
        # print(str3)
        cur.execute(str3)
        returned = cur.fetchone()
        # print(returned[0])
        if(returned[0]==1):
            print("Already att is marked as present , no need to do anything")
        else:   
            print("Initially absent: we need to update both the columns")
            str3 = "UPDATE MAINATT SET \""
            str3 += str(today)
            str3 += "\" =1 WHERE ROLL = "
            str3+= str(rollno)
            str3 += ";"
            cur.execute(str3)
            print("attendence marked in mainatt")
            str3 = "SELECT * FROM SECOND WHERE ROLL = "
            str3 += str(rollno)
            str3+=";"
            cur.execute(str3)
            returned = cur.fetchone()
            attended = returned[1]
            attended = attended+1
            str3 = "UPDATE SECOND SET ATTENDED = "
            str3 += str(attended)
            str3 += " WHERE ROLL = "
            str3 += str(rollno)
            str3 += ";"
            cur.execute(str3)
            print("attended also increased")

    else:
        print("Column Dont Exist")
        str3 = "SELECT * FROM SECOND WHERE ROLL = "
        str3 += str(rollno)
        str3+=";"
        cur.execute(str3)
        returned = cur.fetchone()
        total = returned[2]
        total = total+1
        for v in range(0,students+1):
            str4 = "UPDATE SECOND SET TOTAL ="
            str4 += str(total)
            str4 += "WHERE ROLL ="
            str4 += str(v)
            str4 +=";"
            cur.execute(str4)
            print("updated total column of second")

        str2 = "ALTER TABLE MAINATT ADD COLUMN \""
        str2 += str(today)
        str2 += "\" int;"
        print(str2)
        cur.execute(str2)
        print("New column created")
        for student in range(1,students+1):
            str3 = "UPDATE MAINATT SET \""
            str3 += str(today)
            str3 += "\" =0 WHERE ROLL = "
            str3+= str(student)
            str3 += ";"
            cur.execute(str3)
        str3 = "UPDATE MAINATT SET \""
        str3 += str(today)
        str3 += "\" =1 WHERE ROLL = "
        str3+= str(rollno)
        str3 += ";"
        cur.execute(str3)
        print("attendence marked in mainatt")
        str3 = "SELECT * FROM SECOND WHERE ROLL = "
        str3 += str(rollno)
        str3+=";"
        cur.execute(str3)
        returned = cur.fetchone()
        attended = returned[1]
        attended = attended+1
        str3 = "UPDATE SECOND SET ATTENDED = "
        str3 += str(attended)
        str3 += " WHERE ROLL ="
        str3+= str(rollno)
        str3 += ";"
        cur.execute(str3)
        print("attended also increased")
#arguments must be between 1-5 
# we hane to send rollno as integer in function named 'upload'
upload(5)    

conn.commit()
conn.close()