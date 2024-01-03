from flask import Blueprint, render_template, request, flash, jsonify
from .models import data1, device1
from . import db
from datetime import datetime
import csv
import os
import requests

# Tạo một Blueprint trong Flask
data_export = Blueprint('data_export', __name__)

@data_export.route('/export', methods=['GET'])
# def export_csv():
#     # Lấy tất cả dữ liệu từ bảng data1
#     datas = data1.query.all()

#     # Kiểm tra nếu có ít nhất 1000 dòng dữ liệu
#     if len(datas) >= 1:
#         # Tạo một danh sách để chứa dữ liệu cho CSV
#         csv_data = []

#         # Lặp qua các dòng dữ liệu và thêm chúng vào danh sách
#         for data in datas:
#             # Xử lý mã hóa và tách thành cặp (x, y)
#             processed_data = process_and_split_data(data.data)

#             # Thêm vào danh sách
#             csv_data.extend([(time, value, data.device_id) for time, value in processed_data])

#         # Generate a timestamp for the filename
#         timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
#         # Define the folder path
#         export_folder = 'export_data'
        
#         # Ensure the export folder exists
#         os.makedirs(export_folder, exist_ok=True)

#         # Specify the CSV file path
#         csv_filename = os.path.join(export_folder, f'exported_data_{timestamp}.csv')

#         # Mở file CSV để ghi
#         with open(csv_filename, 'w', newline='') as csvfile:
#             # Sử dụng CSV writer để ghi dữ liệu vào file
#             csv_writer = csv.writer(csvfile)

#             # Ghi header nếu cần thiết
#             csv_writer.writerow(['TIME', 'VALUE', 'Device ID'])

#             # Ghi dữ liệu vào file
#             csv_writer.writerows(csv_data)
        
#         # Make a POST request to /delete_all
#         delete_all_response = requests.post('http://127.0.0.1:8888/delete-all')

#         # Check if the delete_all request was successful
#         if delete_all_response.status_code == 200:
#             # If successful, return a JSON response with success and filename
#             flash('Data exported!', category='success')
#             return jsonify({'success': True, 'filename': csv_filename})
#         else:
#             # If not successful, return a JSON response with an error message
#             flash('Failed to delete all data after export!', category='error')
#             return jsonify({'success': False, 'message': 'Failed to delete all data after export'})
#     else:
#         # Trả về thông báo nếu không đủ dữ liệu
#         flash('Not enough data to export CSV!', category='error')
#         return jsonify({'success': False, 'message': 'Not enough data to export CSV'})
def export_csv():
    # Get all devices
    devices = device1.query.all()
    data_success_count=0
    # Loop through each device
    for device in devices:
        # Get data for the current device
        datas = data1.query.filter_by(mac_adr=device.mac_adr).all()

        # Check if there is at least 1 record
        if len(datas) >= 1:
            # Create a list to store data for CSV
            csv_data = []

            # Loop through the data records and add them to the list
            for data in datas:
                # Process and split the data into (time, value) pairs
                processed_data = process_and_split_data(data.data)

                # Add to the list with 'Mac address'
                csv_data.extend([(time, value) for time, value in processed_data])

            # Generate a timestamp for the filename
            timestamp = datetime.now().strftime('%Y_%m_%d %H_%M_%S')

            # Define the folder path based on the Mac address
            # export_folder = os.path.join('export_data', f'device_{device.id}')
            export_folder = os.path.join('export_data', f'{device.mac_adr.replace(":", "")}')

            # Ensure the export folder exists
            os.makedirs(export_folder, exist_ok=True)

            # Specify the CSV file path
            csv_filename = os.path.join(export_folder, f'exported_data_{timestamp}.csv')

            # Open the CSV file for writing
            with open(csv_filename, 'w', newline='') as csvfile:
                # Use CSV writer to write data to the file
                csv_writer = csv.writer(csvfile)

                # Write header
                csv_writer.writerow(['TIME', 'VALUE'])

                # Write data to the file
                csv_writer.writerows(csv_data)
            data_success_count=data_success_count+1
    if data_success_count>0:
        # Make a POST request to /delete_all
        delete_all_response = requests.post(f'http://127.0.0.1:8888/delete-all')

        # Check if the delete_all request was successful
        if delete_all_response.status_code == 200:
            # If successful, return a JSON response with success and filename
            flash(f'Data exported!', category='success')
            return jsonify({'success': True, 'filename': csv_filename})
        else:
            # If not successful, return a JSON response with an error message
            flash(f'Failed to delete all data after export!', category='error')
            return jsonify({'success': False, 'message': f'Failed to delete all data after export'})
    else:
        # Return a message if there is not enough data for the current device
        flash(f'Not enough data to export CSV!', category='error')
        return jsonify({'success': False, 'message': f'Not enough data to export CSV'})

def process_and_split_data(data_str):
    # Giả sử dữ liệu có định dạng "?x1&y1?x2&y2"
    parts = data_str.split('?')
    
    # Lọc bỏ các phần rỗng
    parts = list(filter(None, parts))

    # Xử lý mã hóa và tách thành cặp (x, y)
    processed_data = [tuple(part.split('&')) for part in parts]

    return processed_data


# # Thêm Blueprint vào ứng dụng Flask
# app.register_blueprint(data_export)
