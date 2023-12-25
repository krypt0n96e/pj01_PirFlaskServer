from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy import and_
from .models import data1,device1
from . import db
import json

esphandle = Blueprint('esphandle', __name__)

@esphandle.route('/esp', methods=['GET','POST'])
def esp_handle():
    if request.method == 'POST':
        try:
            # post_data = request.data.decode('utf-8')
            # post_data = json.loads(request.data)
            # data=post_data['data']
            # device_id=post_data['device_id']
            # print("Received data: ", data, "--- Device id: ",device_id)
            # data = data1(data=data,device_id=device_id)
            # db.session.add(data)
            # db.session.commit()
            
            post_data = request.data.decode('utf-8')
            post_data = json.loads(request.data)
            data=post_data['data']
            mac_adr=post_data['mac_adr']
            print("Received data: ", data, "--- Mac address: ",mac_adr)
            data = data1(data=data,mac_adr=mac_adr)
            db.session.add(data)
            db.session.commit()
        

            return "ok"
        except Exception as e:
            print("Error:", str(e))
            return "error"
    elif request.method == 'GET': #HOST/esp?start=value&end=value&mac_id=value
        start_id = request.args.get('start', type=int)
        end_id = request.args.get('end', type=int)
        # device_id_filter = request.args.get('id', type=int)
        mac_adr_filter = request.args.get('mac_adr', type=str)

        # Use the provided values or set defaults if not present
        start_id = start_id if start_id is not None else 0
        end_id = end_id if end_id is not None else float('inf')

        # if device_id_filter is not None:
        if mac_adr_filter is not None:
            # datas = data1.query.filter(and_(data1.id >= start_id, data1.id <= end_id, data1.device_id == device_id_filter)).all()
            datas = data1.query.filter(and_(data1.id >= start_id, data1.id <= end_id, data1.mac_adr == mac_adr_filter)).all()
        else:
            datas = data1.query.filter(and_(data1.id >= start_id, data1.id <= end_id)).all()

        if datas:
            # data_list = [{"id": entry.id, "data": entry.data, "date": entry.date, "device_id": entry.device_id} for entry in datas]
            data_list = [{"id": entry.id, "data": entry.data, "date": entry.date, "mac_adr": entry.mac_adr} for entry in datas]
            return jsonify(data_list), 200
        else:
            return jsonify({'error': 'Invalid range or no data found'}), 404
        # else:
        #     datas = data1.query.all()
        #     data_list = [{"id": entry.id, "data": entry.data,"date": entry.date, "device_id": entry.device_id} for entry in datas]
        #     return jsonify(data_list), 200
        
@esphandle.route('/device', methods=['GET'])
def device_logs():
    if request.method == 'GET':#HOST/device?id=value?mac_adr=value
        device_id = request.args.get('id', type=int)
        mac_adr = request.args.get('mac_adr', type=str)

        # if device_id is not None:
        if mac_adr is not None:
            # Tìm device theo mac
            device = device1.query.filter_by(mac_adr=mac_adr).first()

            if device:
                # Trả về log của device nếu nó tồn tại
                # return jsonify({'id': device.id, 'logs': device.logs})
                return jsonify({"id": device.id, 'mac_adr': device.mac_adr, 'logs': device.logs})
            else:
                return jsonify({'error': 'Device not found'}), 404
        elif device_id is not None:
            # Tìm device theo ID
            device = device1.query.filter_by(id=device_id).first()

            if device:
                # Trả về log của device nếu nó tồn tại
                # return jsonify({'id': device.id, 'logs': device.logs})
                return jsonify({"id": device.id, 'mac_adr': device.mac_adr, 'logs': device.logs})
            else:
                return jsonify({'error': 'Device not found'}), 404
        else:
            devices = device1.query.all()
            # device_list = [{"id": entry.id, "logs": entry.logs} for entry in devices]
            device_list = [{"id": entry.id, 'mac_adr': entry.mac_adr, 'logs': entry.logs} for entry in devices]
            return jsonify(device_list), 200


@esphandle.route('/assign', methods=['GET'])
def device_assign():
    if request.method == 'GET':
        # # Extract the 'id' parameter from the query string
        # device_id = request.args.get('id', type=int)

        # if device_id is not None:
        #     # Check if a device with the given ID already exists
        #     device = device1.query.filter_by(id=device_id).first()

        #     if device:
        #         # If the device already exists, return an error response
        #         return jsonify({'is_existed': 1, 'log': 'Assign failed!'}),409
        #     else:
        #         # If the device doesn't exist, add it to the database and commit the changes
        #         db.session.add(device1(logs=0, id=device_id))
        #         db.session.commit()
        #         # Return a success response
        #         return jsonify({'is_existed': 0, 'log': 'Assign successful!'}), 200
        # else:
        #     # Handle the case where the 'id' parameter is not provided in the request
        #     return jsonify({'error': 'Invalid get request!'}),400
        # Extract the 'mac_adr' parameter from the query string
        mac_adr = request.args.get('mac_adr', type=str)

        if mac_adr is not None:
            # Check if a device with the given ID already exists
            device = device1.query.filter_by(mac_adr=mac_adr).first()
            if not device:
                # If the device doesn't exist, add it to the database and commit the changes
                db.session.add(device1(logs=0, mac_adr=mac_adr))
                db.session.commit()
                # Return a success response
            return jsonify({'is_assigned': 1, 'log': 'Assign successful!'}), 200
        else:
            # Handle the case where the 'id' parameter is not provided in the request
            return jsonify({'is_assigned': 0, 'log': 'Invalid get request!'}),400
        

                           
            