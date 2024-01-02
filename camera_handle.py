from website.models import camera1
from website import create_app
import cv2
import time
import os
camera_log=0
app = create_app()
def capture_images(output_folder):
    # Mở webcam
    cap = cv2.VideoCapture(0)

    # Kiểm tra xem webcam có được mở không
    if not cap.isOpened():
        print("Error opening webcam.")
        return
    
    count = 0   # Số lượng ảnh đã chụp
    start_time = time.time()
    start_capture_time = 0  # Thời điểm bắt đầu chụp

    # Bắt đầu quay và ghi ảnh
    while True:
        ret, frame = cap.read()

        # Kiểm tra xem frame có được đọc đúng không
        if not ret:
            print("Error in retrieving frame.")
            break

        # Tính thời gian giữa các frame
        elapsed_time = time.time() - start_time

        # Chờ 3 giây trước khi bắt đầu lưu ảnh
        if elapsed_time >= 3 and start_capture_time == 0:
            start_capture_time = time.time()

        # Chụp ảnh sau khi đã chờ 3 giây
        if start_capture_time > 0:
            count += 1
            current_time_str = time.strftime("%Y-%m-%d %H-%M-%S")
            output_file = f'{output_folder}/{count}jpg'

            resized_frame = cv2.resize(frame, (640, 480))
            
            # Hiển thị thời gian trên ảnh
            cv2.putText(resized_frame, current_time_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Lưu ảnh vào thư mục
            cv2.imwrite(output_file, resized_frame)

            # Hiển thị ảnh trong cửa sổ
            cv2.imshow('Captured Image', resized_frame)

            # Đặt lại thời gian bắt đầu cho frame tiếp theo
            start_time = time.time()

        with app.app_context():
            camera = camera1.query.filter_by(id= 1).first()
            camera_log=camera.logs
        # Kiểm tra neu log bang 0 thi dung
        if not camera_log:
            break
        # Kiểm tra phím 'q' để thoát
        if cv2.waitKey(33) == ord('q'):
            break

    # Giải phóng tài nguyên khi kết thúc
    cap.release()
    cv2.destroyAllWindows()
def camera_control():
    while 1:
        with app.app_context():
            camera = camera1.query.filter_by(id= 1).first()
            camera_log=camera.logs
        if camera_log:
            output_folder = f'output_images/start_{time.time():.3f}'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            # Gọi hàm để chụp ảnh và ghi lại mỗi 50ms
            capture_images(output_folder)
