
import cv2
import mediapipe as mp
from pathlib import Path
from collections import deque
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from robot_communication import RobotCommunication


# ================= CONFIGURATION =================

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "hand_landmarker.task"
)

CAMERA_INDEX = 0
ARDUINO_PORT = "COM5"
BAUD_RATE = 9600

STABLE_FRAMES = 5

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

COMMAND_CODES = {
    "FORWARD": "F",
    "BACKWARD": "B",
    "LEFT": "L",
    "RIGHT": "R",
    "STOP": "S"
}


# ================= FINGER COUNTING =================

def count_fingers(landmarks):
    fingers_up = 0

    for tip, pip in zip(
        [8, 12, 16, 20],
        [6, 10, 14, 18]
    ):
        if landmarks[tip].y < landmarks[pip].y:
            fingers_up += 1

    # Thumb rule for mirrored webcam image
    if landmarks[4].x < landmarks[3].x:
        fingers_up += 1

    return fingers_up


# ================= GESTURE MAPPING =================

def get_command(fingers_up):
    commands = {
        0: "STOP",
        1: "BACKWARD",
        2: "FORWARD",
        3: "LEFT",
        4: "RIGHT",
        5: "STOP"
    }

    return commands.get(fingers_up, "STOP")


# ================= DRAW LANDMARKS =================

def draw_hand(frame, landmarks):
    height, width, _ = frame.shape

    points = [
        (int(point.x * width), int(point.y * height))
        for point in landmarks
    ]

    for start, end in HAND_CONNECTIONS:
        cv2.line(
            frame,
            points[start],
            points[end],
            (0, 255, 0),
            2
        )

    for x, y in points:
        cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)


# ================= MAIN PROGRAM =================

def main():
    if not MODEL_PATH.exists():
        print(f"ERROR: Model not found: {MODEL_PATH}")
        return

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        ),
        running_mode=vision.RunningMode.IMAGE,
        num_hands=1
    )

    landmarker = vision.HandLandmarker.create_from_options(options)
    camera = None
    robot = RobotCommunication(
        port=ARDUINO_PORT,
        baud_rate=BAUD_RATE,
        simulation=False
    )

    # Store recent candidate commands
    recent_commands = deque(maxlen=STABLE_FRAMES)
    active_command = "STOP"

    try:
        if not robot.connect():
            return

        camera = cv2.VideoCapture(CAMERA_INDEX)

        if not camera.isOpened():
            print("ERROR: Could not open webcam.")
            return

        print("Arduino connected on COM5.")
        print("Gesture stability filtering enabled.")
        print("Keep motors disconnected. Press Q to quit.")

        while True:
            success, frame = camera.read()

            if not success:
                print("ERROR: Could not read webcam frame.")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            result = landmarker.detect(mp_image)

            fingers_up = None
            candidate_command = None

            if result.hand_landmarks:
                landmarks = result.hand_landmarks[0]
                draw_hand(frame, landmarks)

                fingers_up = count_fingers(landmarks)
                candidate_command = get_command(fingers_up)

                # Accept a command only after consecutive matching frames
                recent_commands.append(candidate_command)

                if (
                    len(recent_commands) == STABLE_FRAMES
                    and all(
                        item == recent_commands[0]
                        for item in recent_commands
                    )
                ):
                    active_command = recent_commands[0]

                cv2.putText(
                    frame,
                    "Hand Detected!",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Fingers: {fingers_up}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Candidate: {candidate_command}",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 200, 0),
                    2
                )

            else:
                # Fail safe: missing hand means STOP immediately
                recent_commands.clear()
                active_command = "STOP"

                cv2.putText(
                    frame,
                    "No Hand - STOP",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            arduino_command = COMMAND_CODES[active_command]
            robot.send_command(arduino_command)

            cv2.putText(
                frame,
                f"Active: {active_command}",
                (20, 165),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Arduino code: {arduino_command}",
                (20, 205),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.imshow(
                "Hand Gesture Controlled Robot",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except (RuntimeError, OSError) as error:
        print(f"ERROR: {error}")

    finally:
        robot.disconnect()

        if camera is not None:
            camera.release()

        cv2.destroyAllWindows()
        landmarker.close()
        print("Program stopped.")


if __name__ == "__main__":
    main()
