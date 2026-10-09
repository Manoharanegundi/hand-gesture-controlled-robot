
import cv2
import mediapipe as mp
import time

SERIAL_TEST_MODE = True
last_sent_command = None
last_sent_time = 0

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

print("Starting hand detection...")

# Load the downloaded hand model
model_path = "models/hand_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=model_path
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)

# Start webcam
camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        print("Could not access camera")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    result = detector.detect(mp_image)

    if result.hand_landmarks:
        height, width, _ = frame.shape
        cv2.putText(
    frame,
    "Hand Detected!",
    (20, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

        for hand_landmarks in result.hand_landmarks:
            fingers_up = 0
            
            
            # Detect thumb using distance from its base
            thumb_tip = hand_landmarks[4]
            thumb_ip = hand_landmarks[3]
            thumb_mcp = hand_landmarks[2]
            index_mcp = hand_landmarks[5]

            # Distance from thumb tip and joint to index-finger base
            tip_distance = (
                (thumb_tip.x - index_mcp.x) ** 2
                + (thumb_tip.y - index_mcp.y) ** 2
            ) ** 0.5

            joint_distance = (
                (thumb_ip.x - index_mcp.x) ** 2
                + (thumb_ip.y - index_mcp.y) ** 2
            ) ** 0.5

            if tip_distance > joint_distance * 1.2:
                
                fingers_up += 1

            
          

            
            # Count the other four fingers
            finger_tips = [8, 12, 16, 20]
            finger_pips = [6, 10, 14, 18]

            for tip, pip in zip(finger_tips, finger_pips):
                if hand_landmarks[tip].y < hand_landmarks[pip].y:
                    fingers_up += 1

            # Display finger count
            cv2.putText(
                frame,
                f"Fingers: {fingers_up}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            ) 
            
            # Convert finger count into a robot command
            
            if fingers_up == 0 or fingers_up == 5:
                command = "S"
                command_name = "STOP"
            elif fingers_up == 1:
                command = "F"
                command_name = "FORWARD"
            elif fingers_up == 2:
                command = "B"
                command_name = "BACKWARD"
            elif fingers_up == 3:
                command = "L"
                command_name = "LEFT"
            elif fingers_up == 4:
                command = "R"
                command_name = "RIGHT"
            else:
                command = "S"
                command_name = "STOP"

                        # Software-only test: simulate sending commands
            current_time = time.time()

            if (
                command != last_sent_command
                or current_time - last_sent_time >= 1
            ):
                if SERIAL_TEST_MODE:
                    print(f"Test command: {command} ({command_name})")

                last_sent_command = command
                last_sent_time = current_time

            # Display the robot command
            
            cv2.putText(
                frame,
                f"Command: {command_name}",
                (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )
            # Draw green dots on the hand
            for landmark in hand_landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # Connect the finger landmarks
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (5, 6), (6, 7), (7, 8),
                (0, 9), (9, 10), (10, 11), (11, 12),
                (0, 13), (13, 14), (14, 15), (15, 16),
                (0, 17), (17, 18), (18, 19), (19, 20),
                (5, 9), (9, 13), (13, 17)
            ]

            for start, end in connections:
                x1 = int(hand_landmarks[start].x * width)
                y1 = int(hand_landmarks[start].y * height)
                x2 = int(hand_landmarks[end].x * width)
                y2 = int(hand_landmarks[end].y * height)

                cv2.line(
                    frame, (x1, y1), (x2, y2),
                    (0, 255, 0), 2
                )

    cv2.imshow("Hand Gesture Robot", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
detector.close()
cv2.destroyAllWindows()