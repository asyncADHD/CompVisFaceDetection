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
                # Draw landmarks on the frame
                for landmark in landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                    # Check if the index finger (landmark 8) is within the tracking box
                    if box_x < x < box_x + box_width and box_y < y < box_y + box_height:
                        # Activate volume control logic here
                        # You can set a flag to indicate that the hand is inside the box
                        # and use that flag in your volume control logic.
                        print("TRACKING ACTIVATED")


        # Draw the tracking box on the frame
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 255), 2)

        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
