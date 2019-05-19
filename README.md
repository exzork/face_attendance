# face_attendance
Face Attendance System
Using :
1. Python 3.7 (dlib,opencv,numpy,os,mysql.connector,datetime,scipy,imutils,time)
2. Php 7.0
3. MariaDB

Change line 31-34 based on your database.
Change line 49 according to your IPCam (I using IPCam here), or Webcam(change src=0) to use default webcam attached.
You need to add member to database before launching face_recog_webcam.py.
Every new member added, face_recog_webcam.py need to be relaunched.
