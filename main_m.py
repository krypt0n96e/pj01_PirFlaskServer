from multiprocessing import Process, Manager
from website import create_app
from website.models import camera1
import requests
import cv2
import time
import os
import numpy as np

app = create_app()

def display_video(frame_queue, stop_flag):
    cv2.namedWindow('Recording Video', cv2.WINDOW_NORMAL)
    while not stop_flag.is_set():
        try:
            frame = frame_queue.get()
            if frame is not None:
                # Display the frame
                cv2.imshow('Recording Video', frame)
                cv2.waitKey(1)
        except KeyboardInterrupt:
            break
    cv2.destroyAllWindows()

def camera_control(frame_queue, stop_flag):
    while not stop_flag.is_set():
        try:
            with app.app_context():
                camera = camera1.query.filter_by(id=1).first()
                log_value = camera.logs

            if log_value:
                output_folder = 'output_videos'

                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                cap = cv2.VideoCapture(0)

                if not cap.isOpened():
                    print("Error opening webcam.")
                    return

                fps = cap.get(cv2.CAP_PROP_FPS)
                delay = int(1000 / fps)

                frame_width = int(cap.get(3))
                frame_height = int(cap.get(4))

                output_file = f'{output_folder}/video_output_start_{time.time():.3f}.avi'
                out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

                while log_value:
                    ret, frame = cap.read()

                    if not ret:
                        print("Error in retrieving frame.")
                        break

                    current_time_str = time.strftime("%Y:%m:%d %H:%M:%S")
                    cv2.putText(frame, current_time_str, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(frame, f"{time.time():.3f}", (300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(frame, f"Webcam FPS: {fps}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    out.write(frame)

                    frame_queue.put(frame)

                    if cv2.waitKey(delay) == ord('q'):
                        break

                    with app.app_context():
                        camera = camera1.query.filter_by(id=1).first()
                        log_value = camera.logs

                cap.release()
                out.release()
        except KeyboardInterrupt:
            break

    print("Camera control process stopped.")

def run_flask():
    app.run(host='0.0.0.0', port=8888)

def export():
    while True:
        time.sleep(3600)
        try:
            # Make an HTTP GET request to 127.0.0.1/export
            response = requests.get('http://127.0.0.1:8888/export')

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                print('----------------------------Data_Exported!------------------------')
            else:
                print(f'Error: Failed to fetch data. Status Code: {response.status_code}')
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    # Create a flag for stopping the camera_control process
    stop_flag = Manager().Event()

    # Create a queue for passing frames between processes
    frame_queue = Manager().Queue()

    # Start the display process
    display_process = Process(target=display_video, args=(frame_queue, stop_flag))
    display_process.start()

    # Start other processes
    flask_process = Process(target=run_flask)
    export_process = Process(target=export)
    camera_process = Process(target=camera_control, args=(frame_queue, stop_flag))

    # Start all processes
    flask_process.start()
    export_process.start()
    camera_process.start()

    try:
        # Main process logic
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Set the stop flag to terminate the camera_control process
        stop_flag.set()

        # Gracefully terminate the processes
        display_process.terminate()
        flask_process.terminate()
        export_process.terminate()
        camera_process.terminate()

        # Wait for the processes to finish
        display_process.join()
        flask_process.join()
        export_process.join()
        camera_process.join()
