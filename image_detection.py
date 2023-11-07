# image_detection.py
import cv2
import mediapipe as mp


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
                # Draw landmarks on the frame
                for landmark in landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()
