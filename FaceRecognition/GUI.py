import tkinter as tk
import os
import cv2
import numpy as np
from PIL import Image
import sqlite3 as lite
import sys
import psycopg2
from datetime import date
conn = psycopg2.connect(database = "testdb2", user = "postgresql", password = "namespace1", host = "sample-database.czgprnseypbr.us-east-1.rds.amazonaws.com", port = "5432")
print ('Opened database successfully')
cur = conn.cursor()

con=lite.connect('StudentDetail.db')

names = ['None']
def faceDataset(ID,Name):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # For each person, enter one numeric face id
    face_id = ID
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0
    while(True):
        ret, img = cam.read()
        #img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 15: # Take 30 face sample and stop video
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    with con:
        cur = con.cursor()    
        cur.execute("CREATE TABLE IF NOT EXISTS student(Id INT, Name TEXT)")
        cur.execute("INSERT INTO student VALUES(?,?)",(ID,Name))
        print(int(ID))
        names.insert(int(ID),Name)

def trainFace():
    path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
    # function to get the images and label data
    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples,ids
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

attendance=set()
def attendanceID(roll):
    attendance.add(roll)

def upload(rollno):
    today = str(date.today())
    # print(today)


    students = 40

    #today = "2019-03-31"
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
            print("Already Att is marked as present , no need to do anything.")
        else:   
            print("Initially Absent: we need to update both the columns.")
            str3 = "UPDATE MAINATT SET \""
            str3 += str(today)
            str3 += "\" =1 WHERE ROLL = "
            str3+= str(rollno)
            str3 += ";"
            cur.execute(str3)
            print("Attendence marked in main attendace.")
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
            print("Attended also increased.")

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

        str2 = "ALTER TABLE MAIN ATTENDANCE ADD COLUMN \""
        str2 += str(today)
        str2 += "\" int;"
        print(str2)
        cur.execute(str2)
        print("New column created")
        for student in range(1,students+1):
            str3 = "UPDATE MAIN ATTENDANCE SET \""
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
        print("Attendence marked in Main Attendance.")
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
        print("Attended also increased.")
    conn.commit()
    

def recognizeFace():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    #iniciate id counter
    id = 0
    # names related to ids: example ==> Marcelo: id=1,  etc
    #names = ['None', 'Adhish', 'Paula', 'Ilza', 'Z', 'W'] 
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        ret, img =cam.read()
        #img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                attendanceID(id)
                #id = names[id]
                confidence = "  {0}%".format(round(100 - confidence)) 
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
        
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    

class GUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Classroom Attendance')
        self.label=tk.Label(self, text='Roll No.')
        self.label.pack()
        self.entry = tk.Entry(self,width=35)
        self.entry.pack()
        self.label2=tk.Label(self, text='Name')
        self.label2.pack()
        self.entry2 = tk.Entry(self,width=35)
        self.entry2.pack()
        self.button = tk.Button(self, text="Create User Dataset",width=35, command=self.on_button1)
        self.button.pack()
        self.button = tk.Button(self, text="Train Dataset",width=35, command=self.on_button2)
        self.button.pack()
        self.button = tk.Button(self, text="Take Attendance",width=35, command=self.on_button3)
        self.button.pack()
        

    def on_button1(self):
        userID=self.entry.get()
        userName=self.entry2.get()
        faceDataset(userID,userName)

    def on_button2(self):
        trainFace()
    
    def on_button3(self):
        recognizeFace()



w = GUI()
w.mainloop()
print(attendance)
for i in attendance:
    upload(i)
conn.commit()
conn.close()