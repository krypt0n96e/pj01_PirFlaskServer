import cv2
import time
import os
from website.models import camera1
from website import create_app

app = create_app()
camera_log = 0
camera_id=1

def capture_images(output_folder):
    sub_output = f'{output_folder}/record_{time.strftime("%Y_%m_%d %H_%M_%S")}'
    os.makedirs(sub_output)
    
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
            
            output_file = f'{sub_output}/{count}.jpg'  # Use JPEG format

            # Resize the frame to reduce resolution
            resized_frame = cv2.resize(frame, (640, 480))  # Adjust the resolution as needed

            cv2.putText(resized_frame, current_time_str, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(resized_frame, f"{time.time():.3f}", (400, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Save the resized and compressed frame as JPEG
            cv2.imwrite(output_file, resized_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

            cv2.imshow('Captured Image', resized_frame)

            start_time = time.time()

        with app.app_context():
            camera = camera1.query.filter_by(id=camera_id).first()
            camera_log = camera.logs

        if not camera_log:
            break

        if cv2.waitKey(20) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
def record_video(output_folder):
    # Mở webcam
    cap = cv2.VideoCapture(0)
    

    # Kiểm tra xem webcam có được mở không
    if not cap.isOpened():
        print("Error opening webcam.")
        return

    # Lấy thông số của video từ webcam
    # fps = cap.get(cv2.CAP_PROP_FPS)
    fps = 15
    delay = int(1000 / fps)  # Thời gian chờ tính theo milliseconds 

    # Lấy thông số của video từ webcam
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Tạo đối tượng VideoWriter với tốc độ khung hình giảm xuống 10.0
    output_file = f'{output_folder}/record_{time.strftime("%Y_%m_%d %H_%M_%S")}.mp4'
    # out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width , frame_height))


    # Bắt đầu quay và ghi video
    while True:
        ret, frame = cap.read()

        # Kiểm tra xem frame có được đọc đúng không
        if not ret:
            print("Error in retrieving frame.")
            break

        # Hiển thị thời gian trên video
        current_time_str = time.strftime("%Y:%m:%d %H:%M:%S")
        cv2.putText(frame, current_time_str+f"/{time.time():.3f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        # cv2.putText(frame, f"{time.time():.3f}", (300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.putText(frame, f"Webcam FPS: {fps}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Ghi frame vào video
        out.write(frame)

        # Hiển thị video trong cửa sổ
        cv2.imshow('Recording Video', frame)

        # Kiểm tra phím 'q' để thoát
        if cv2.waitKey(delay) == ord('q'):
            break

        with app.app_context():
            camera = camera1.query.filter_by(id=camera_id).first()
            camera_log = camera.logs

        # Kiểm tra nếu log bằng 0 thì dừng ghi video
        if not camera_log:
            break

    # Giải phóng tài nguyên khi kết thúc
    cap.release()
    out.release()
    cv2.destroyAllWindows()
def camera_control():
    while True:
        with app.app_context():
            camera = camera1.query.filter_by(id=camera_id).first()
            camera_log = camera.logs

        if camera_log:
            output_folder = f'output_capture/camera_{camera_id}'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # capture_images(output_folder)
            record_video(output_folder)