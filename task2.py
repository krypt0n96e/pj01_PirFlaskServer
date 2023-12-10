import time
import requests

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

