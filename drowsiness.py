import cv2
import mediapipe as mp
import time
import serial

arduino = serial.Serial('COM5', 9600)
time.sleep(2)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):
    vertical = abs(eye[1].y - eye[5].y) + abs(eye[2].y - eye[4].y)
    horizontal = abs(eye[0].x - eye[3].x)
    return vertical / horizontal

closed_start = None
motor_stopped = False
DROWSY_TIME = 2.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        lm = result.multi_face_landmarks[0].landmark

        left = [lm[i] for i in LEFT_EYE]
        right = [lm[i] for i in RIGHT_EYE]

        ear = (eye_aspect_ratio(left) + eye_aspect_ratio(right)) / 2

        # 👀 EYES CLOSED
        if ear < 0.25:
            if closed_start is None:
                closed_start = time.time()

            elif time.time() - closed_start > DROWSY_TIME and not motor_stopped:
                arduino.write(b'0')   # STOP motor
                motor_stopped = True
                print("EYES CLOSED → MOTOR STOPPED")

        # 👀 EYES OPEN
        else:
            closed_start = None
            if motor_stopped:
                arduino.write(b'1')   # RUN motor
                motor_stopped = False
                print("EYES OPEN → MOTOR RUNNING")

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
