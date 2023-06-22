import cv2
import time
import threading

# Load the Haar cascade file for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define global state variables
paused = False
consecutive_pomodoros = 0

def is_user_present():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read the current frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # If a face is detected, the user is present
        if len(faces) > 0:
            # Draw a green rectangle around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            print("You left your seat. Get back to work!")

        # Display the image
        cv2.imshow('Video', frame)

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()
    return False


def pomodoro_timer(minutes):
    global paused
    global consecutive_pomodoros

    end_time = time.time() + minutes * 60  # End time in seconds

    while time.time() < end_time:
        if paused:
            print("Timer is paused. Press 'r' to resume.")
            time.sleep(5)
            continue

        if not is_user_present():
            print("You left your seat. Get back to work!")
            consecutive_pomodoros = 0  # Reset the count
        else:
            time.sleep(5)  # Check again in 5 seconds

    consecutive_pomodoros += 1
    print("Pomodoro complete! Take a short break.")
    if consecutive_pomodoros > 1:
        print(f"Great job! You've completed {consecutive_pomodoros} Pomodoros without leaving your seat.")

def user_interface():
    global paused

    while True:
        command = input("Enter 'p' to pause, 'r' to resume, or 'q' to quit: ")
        if command == 'p':
            paused = True
        elif command == 'r':
            paused = False
        elif command == 'q':
            print("Quitting the program.")
            break

# Run the user interface and the Pomodoro timer in separate threads
threading.Thread(target=user_interface).start()
threading.Thread(target=pomodoro_timer, args=(25,)).start()
