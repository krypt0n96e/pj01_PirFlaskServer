from website.models import camera1
from website import create_app
import cv2
import time
import os

camera_log = 0
app = create_app()

def capture_images(output_folder):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error opening webcam.")
        return

    count = 0
    start_time = time.time()
    start_capture_time = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error in retrieving frame.")
            break

        elapsed_time = time.time() - start_time

        if elapsed_time >= 3 and start_capture_time == 0:
            start_capture_time = time.time()

        if start_capture_time > 0:
            count += 1
            current_time_str = time.strftime("%Y:%m:%d %H:%M:%S")
            output_file = f'{output_folder}/{count}.jpg'  # Fixed file path concatenation

            resized_frame = cv2.resize(frame, (640, 480))

            cv2.putText(resized_frame, current_time_str, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(resized_frame, f"{time.time():.3f}", (400, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imwrite(output_file, resized_frame)
            cv2.imshow('Captured Image', resized_frame)

            start_time = time.time()

        with app.app_context():
            camera = camera1.query.filter_by(id=1).first()
            camera_log = camera.logs
            # print(f"Camera logs: {camera_log}")

        if not camera_log:
            # print("Camera log is 0. Stopping capture.")
            break

        if cv2.waitKey(33) == ord('q'):
            # print("User pressed 'q'. Stopping capture.")
            break

    cap.release()
    cv2.destroyAllWindows()

def camera_control():
    while 1:
        with app.app_context():
            camera = camera1.query.filter_by(id=1).first()
            camera_log = camera.logs
            # print(f"Camera logs: {camera_log}")

        if camera_log:
            output_folder = f'output_images/start_{time.time():.3f}'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # print(f"Capturing images to folder: {output_folder}")
            capture_images(output_folder)

# camera_control()
