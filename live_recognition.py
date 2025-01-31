import cv2
import face_recognition as fr
import numpy as np
from database import load_faces_from_db

face_recognition_running = False

def live_face_recognition():
    """Perform live face recognition using the webcam."""
    global face_recognition_running
    known_names, known_encodings = load_faces_from_db()
    video_capture = cv2.VideoCapture(0)

    face_recognition_running = True
    while face_recognition_running:
        ret, frame = video_capture.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

        face_locations = fr.face_locations(small_frame)
        face_encodings = fr.face_encodings(small_frame, face_locations)

        for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
            face_distances = fr.face_distance(known_encodings, encoding)
            best_match_index = np.argmin(face_distances)
            name = "Unknown"

            if face_distances[best_match_index] < 0.6:
                name = known_names[best_match_index]

            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Live Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    face_recognition_running = False

def stop_face_recognition():
    """Stop the face recognition process."""
    global face_recognition_running
    face_recognition_running = False
