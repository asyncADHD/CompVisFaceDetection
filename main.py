# main.py
from image_detection import init_webcam, detect_hands


def main():
    cap = init_webcam()
    detect_hands(cap)

if __name__ == "__main__":
    main()
