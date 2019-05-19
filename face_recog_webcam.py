import face_recognition
import cv2
import numpy as np
import os
import mysql.connector as mc
import datetime
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import dlib
import time
def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
d=datetime.datetime.now()
mydb = mc.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "face_login"
    )
db = mydb.cursor()
COUNTER =0
TOTAL =0
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = VideoStream(src="http://192.168.0.120:8080/video").start()

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
#Determine some Variable
EYE_AR_THRESH=0.27
EYE_AR_CONSEC_FRAMES = 2
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#Grab eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
#Known Faces
arr_knownface = os.listdir("./known_face")
for filename in arr_knownface:
    name = filename[:-4]
    known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file("./known_face/"+filename))[0])
    known_face_names.append(name)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
text=""
while True:
    # Grab a single frame of video
    frame = video_capture.read()
    frame2 = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
        # loop over the face detections
    for rect in rects:
         # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy            # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
    
            # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0
    
            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
    
            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:
            COUNTER += 1
    
            # otherwise, the eye aspect ratio is not below the blink
            # threshold
        else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
               TOTAL += 1
    
                # reset the eye frame counter
            COUNTER = 0
    
            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the fr
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]


    # Only process every other frame of video to save time
    if process_this_frame:

        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                db.execute("SELECT id,name FROM face_id where id ="+name)
                result_db = db.fetchone()
                name_face=result_db[1]
                face_names.append(name_face)
                id_face=result_db[0]
                db.execute("SELECT face_id,date_log FROM date_attendance where face_id='"+str(id_face)+"' AND date_log='"+str(d.year)+"-"+f"{d.month:02d}"+"-"+f"{d.day:02d}"+"'")
                db.fetchall()
                if db.rowcount<1 :
                    if TOTAL > 0:
                        db.execute("INSERT INTO date_attendance(face_id,date_log,time_log) VALUES('"+str(name)+"','"+str(d.year)+"-"+f"{d.month:02d}"+"-"+f"{d.day:02d}"+"','"+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+"')")
                        mydb.commit()
                    else:
                        text = "Hello "+name_face+" Please Blink Your Eye Slowly"
                else:
                    text = name_face+" you already attendace today"
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.putText(frame, text, (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

    # Display the resulting image
    cv2.imshow('Face Recognition System', frame)

    # Hit 'q' on the keyboard to quit!
    key = cv2.waitKey(1) & 0xFF
     
        # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break
    

# Release handle to the webcam
video_capture.stop()
cv2.destroyAllWindows()