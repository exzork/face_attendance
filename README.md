# face_attendance
Face Attendance System
Using :
1. Python 3.7 (face_recognition,dlib,opencv,numpy,os,mysql.connector,datetime,scipy,imutils,time)
2. Php 7.0
3. MariaDB

Change line 31-34 based on your database.
Change line 49 according to your IPCam (I using IPCam here), or Webcam(change src=0) to use default webcam attached.
You need to add member to database before launching face_recog_webcam.py.
Every new member added, face_recog_webcam.py need to be relaunched.

You must add minimal 1 face to prevent programs crash.

-5/20/2019 Added eye blink detection 3 time to prevent using photo for recognition
