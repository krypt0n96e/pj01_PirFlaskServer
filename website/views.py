from flask import Blueprint, render_template, request, flash, jsonify
from .models import data1,device1,camera1
from . import db
import json

views = Blueprint('views', __name__)


# @views.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'GET':#HOST?id=[1,2,3]
#         device_ids=
#     else: device_ids = [1, 2]
#     for device_id in device_ids:
#         log = device1.query.filter_by(id=device_id).first()
#         if not log:
#             db.session.add(device1(logs=0, id=device_id))  # Fix: add id=device_id
#         db.session.commit()
#     # if request.method == 'POST': 
#     #     rawdata = request.form.get('data')#Gets the data from the HTML
#     #     rawid = request.form.get('device_id')#Gets the id from the HTML 
#     #     data = data1(data=rawdata,device_id=rawid)  #providing the schema for the data
#     #     db.session.add(data) #adding the data to the database 
#     #     db.session.commit()
#     #     flash('Data added!', category='success')
#     # datas = data1.query.all()  # Retrieve all datas from the database

#     logs = device1.query.all()
#     return render_template("home.html", log=logs)
@views.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'GET':#HOST?id=id1,id2
    #     # Lấy giá trị của 'id' từ query string
    #     device_ids_param = request.args.get('id')

    #     # Kiểm tra nếu 'id' tồn tại trong query string
    #     if device_ids_param:
    #         # Chuyển đổi giá trị 'id' từ chuỗi thành list
    #         device_ids = [int(id) for id in device_ids_param.split(',')]
    #     else:
    #         device_ids = [1]  # Hoặc có thể cung cấp giá trị mặc định nếu 'id' không tồn tại
    # for device_id in device_ids:
    #     log = device1.query.filter_by(id=device_id).first()
    #     if not log:
    #         db.session.add(device1(logs=0, id=device_id))
    #     db.session.commit()
    # logs=[]
    # for device_id in device_ids:
    #     log = device1.query.filter_by(id=device_id).first()
    #     logs.append(log)
    
    if request.method == 'GET':
        camera_ids = [1]
    for camera_id in camera_ids:
        log = camera1.query.filter_by(id=camera_id).first()
        if not log:
            db.session.add(camera1(logs=0, id=camera_id))
            db.session.commit()
    logs = device1.query.all()
    logs_2=camera1.query.all()
    return render_template("home.html", logs=logs,logs_2=logs_2)

@views.route('/delete-data', methods=['POST'])
def delete_data():  
    data = json.loads(request.data)
    dataId = data['dataId']
    data = data1.query.get(dataId)
    if data:
        db.session.delete(data)
        db.session.commit()
    flash('Data deleted!', category='success')
    return jsonify({})

@views.route('/delete-all', methods=['POST'])
def delete_all():  
    try:
        data_objects = data1.query.all()
        for data in data_objects:
            db.session.delete(data)
        db.session.commit()
        flash('All data deleted!', category='success')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({})

@views.route('/reset-all', methods=['POST'])
def reset_all():  
    try:
        decive_objects = device1.query.all()
        for device in decive_objects:
            db.session.delete(device)
        db.session.commit()
        flash('All device reseted!', category='success')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({})

@views.route('/delete-device', methods=['POST'])
def delete_device():  
    data = json.loads(request.data)
    device_id = data['id']
    device = device1.query.get(device_id)
    if device:
        db.session.delete(device)
        db.session.commit()
    flash('Device deleted!', category='success')
    return jsonify({})

@views.route('/turn-on-all', methods=['POST'])
def turn_on_all():  
    try:
        device_objects = device1.query.all()
        for device in device_objects:
            device.logs = 1  # Gán giá trị 1 cho logs (đặt tình trạng bật)
        db.session.commit()
        flash('All devices turned on!', category='success')
        camera_objects = camera1.query.all()
        for camera in camera_objects:
            camera.logs = 1  # Gán giá trị 1 cho logs (đặt tình trạng bật)
        db.session.commit()
        flash('All cameras turned on!', category='success')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({})

@views.route('/turn-off-all', methods=['POST'])
def turn_on_off():  
    try:
        device_objects = device1.query.all()
        for device in device_objects:
            device.logs = 0
        db.session.commit()
        flash('All devices turned off!', category='success')
        camera_objects = camera1.query.all()
        for camera in camera_objects:
            camera.logs = 0
        db.session.commit()
        flash('All cameras turned off!', category='success')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({})

@views.route('/status-change', methods=['POST'])
def status_change():
    data = json.loads(request.data)
    device_id = data['device_id']
    log = data['log']

    req = device1.query.filter_by(id=device_id).first()
    req.logs = log
    db.session.commit()

    return jsonify({})

@views.route('/delete-camera', methods=['POST'])
def delete_camera():  
    data = json.loads(request.data)
    camera_id = data['id']
    camera = camera1.query.get(camera_id)
    if camera:
        db.session.delete(camera)
        db.session.commit()
    flash('Camera deleted!', category='success')
    return jsonify({})


@views.route('/camera-turn', methods=['POST'])
def camera_turn():
    data = json.loads(request.data)
    camera_id = data['camera_id']
    log_2 = data['log_2']

    req = camera1.query.filter_by(id=camera_id).first()
    req.logs = log_2
    db.session.commit()

    return jsonify({})