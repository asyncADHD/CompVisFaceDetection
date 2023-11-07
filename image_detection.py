# image_detection.py
import cv2
import mediapipe as mp


# Define the coordinates and size of the tracking box
box_x = 50  # X-coordinate of the top-left corner
box_y = 50  # Y-coordinate of the top-left corner
box_width = 100  # Width of the box
box_height = 100  # Height of the box


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

                    # Check if the index finger is within the tracking box
                    if box_x < x < box_x + box_width and box_y < y < box_y + box_height:
                        print("Index finger is inside the tracking box")

        # Draw the tracking box on the frame
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 255), 2)

        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
