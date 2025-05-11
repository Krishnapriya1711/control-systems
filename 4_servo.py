#THIS CODE IS FOR ALL 4 SERVO MOTORS


import cv2
import mediapipe as mp
import serial
import time
import math

# Initialize serial communication
ser = serial.Serial('COM3', 9600)  # Change COM port if needed
time.sleep(2)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, model_complexity=1)
mp_draw = mp.solutions.drawing_utils

# Distance between two points
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# State variables to avoid repeated serial writes
prev_state_m1 = None
prev_state_m2 = None
prev_state_m3 = None
prev_state_m4 = None

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    h, w, _ = frame.shape

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # 'Left' or 'Right'
            lm = hand_landmarks.landmark

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = (int(lm[4].x * w), int(lm[4].y * h))
            index_tip = (int(lm[8].x * w), int(lm[8].y * h))
            middle_tip = (int(lm[12].x * w), int(lm[12].y * h))

            # Normalize threshold based on palm size
            wrist = (int(lm[0].x * w), int(lm[0].y * h))
            middle_base = (int(lm[9].x * w), int(lm[9].y * h))
            palm_size = distance(wrist, middle_base)
            threshold = palm_size * 0.4  # dynamic threshold

            if label == 'Right':
                dist_index = distance(thumb_tip, index_tip)
                dist_middle = distance(thumb_tip, middle_tip)

                state_m1 = 0 if dist_index < threshold else 90
                state_m2 = 0 if dist_middle < threshold else 90

                if state_m1 != prev_state_m1:
                    ser.write(f"M1:{state_m1}\n".encode())
                    print(f"[Right Hand] Motor 1: {state_m1} (Distance: {dist_index:.1f})")
                    prev_state_m1 = state_m1

                if state_m2 != prev_state_m2:
                    ser.write(f"M2:{state_m2}\n".encode())
                    print(f"[Right Hand] Motor 2: {state_m2} (Distance: {dist_middle:.1f})")
                    prev_state_m2 = state_m2

            elif label == 'Left':
                dist_index = distance(thumb_tip, index_tip)
                dist_middle = distance(thumb_tip, middle_tip)

                state_m3 = 0 if dist_index < threshold else 90
                state_m4 = 45 if dist_middle < threshold else 0  # Gripper control

                if state_m3 != prev_state_m3:
                    ser.write(f"M3:{state_m3}\n".encode())
                    print(f"[Left Hand] Motor 3: {state_m3} (Distance: {dist_index:.1f})")
                    prev_state_m3 = state_m3

                if state_m4 != prev_state_m4:
                    ser.write(f"M4:{state_m4}\n".encode())
                    print(f"[Left Hand] Motor 4 (Gripper): {state_m4} (Distance: {dist_middle:.1f})")
                    prev_state_m4 = state_m4

    cv2.imshow("4-Motor Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
