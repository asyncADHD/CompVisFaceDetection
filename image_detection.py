# image_detection.py
import cv2
import mediapipe as mp
import subprocess

# Define the coordinates and size of the tracking boxes
volume_up_box = (50, 50, 100, 100)  # (x, y, width, height)
volume_down_box = (200, 50, 100, 100)  # (x, y, width, height)

# Define the box colors
volume_up_box_color = (0, 255, 0)  # Green
volume_down_box_color = (0, 0, 255)  # Red


def init_webcam():
    """
    Initialize and return a capture object for the default camera (usually the built-in webcam).

    Returns:
        cv2.VideoCapture: A capture object for the webcam.
    """
    cap = cv2.VideoCapture(0)
    return cap


def detect_hands(cap):
    """
    Detect and display hand landmarks in the webcam feed.

    Args:
        cap (cv2.VideoCapture): A capture object for the webcam.
    """
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read a frame")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Check if the hand has at least 8 landmarks (including the index finger)
                if len(landmarks.landmark) >= 8:
                    # Get the index finger landmark (landmark 8)
                    index_finger = landmarks.landmark[8]
                    x, y = int(index_finger.x * frame.shape[1]), int(index_finger.y * frame.shape[0])

                    # Check if the index finger is within the volume up box
                    if (volume_up_box[0] < x < volume_up_box[0] + volume_up_box[2] and
                            volume_up_box[1] < y < volume_up_box[1] + volume_up_box[3]):
                        print("Index finger is inside the volume up box")

                        # Increase the volume using AppleScript
                        applescript_command = 'set volume output volume (output volume of (get volume settings) + 5)'
                        subprocess.Popen(['osascript', '-e', applescript_command])

                    # Check if the index finger is within the volume down box
                    if (volume_down_box[0] < x < volume_down_box[0] + volume_down_box[2] and
                            volume_down_box[1] < y < volume_down_box[1] + volume_down_box[3]):
                        print("Index finger is inside the volume down box")

                        # Decrease the volume using AppleScript
                        applescript_command = 'set volume output volume (output volume of (get volume settings) - 5)'
                        subprocess.Popen(['osascript', '-e', applescript_command])

        # Draw the tracking boxes on the frame with labels
        cv2.rectangle(frame, (volume_up_box[0], volume_up_box[1]),
                      (volume_up_box[0] + volume_up_box[2], volume_up_box[1] + volume_up_box[3]),
                      volume_up_box_color, 2)
        cv2.putText(frame, "Volume Up", (volume_up_box[0], volume_up_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    volume_up_box_color, 2)

        cv2.rectangle(frame, (volume_down_box[0], volume_down_box[1]),
                      (volume_down_box[0] + volume_down_box[2], volume_down_box[1] + volume_down_box[3]),
                      volume_down_box_color, 2)
        cv2.putText(frame, "Volume Down", (volume_down_box[0], volume_down_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    volume_down_box_color, 2)

        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()