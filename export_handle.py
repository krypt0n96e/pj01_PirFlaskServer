import time
import requests
from website.models import camera1
from website import create_app

app = create_app()


def export():
    camera_log=0
    camera_id=1
    while True:
        start_time=time.time()
        with app.app_context():
                camera = camera1.query.filter_by(id=camera_id).first()
                camera_log = camera.logs
        while camera_log:
            with app.app_context():
                camera = camera1.query.filter_by(id=camera_id).first()
                camera_log = camera.logs

            # Kiểm tra fdieu kien dừng ghi video
            if not camera_log or (time.time()-start_time>3600):
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
                break
        

