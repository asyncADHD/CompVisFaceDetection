import cv2

def capture_webcam():
    # Open the default camera (usually the built-in webcam)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        if not ret:
            print("Error: Could not read a frame")
            break

        # Display the frame in a window
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
