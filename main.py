from multiprocessing import Process,Lock
from flask_server import run_flask
from export_handle import export
from camera_handle import camera_control

        
if __name__ == '__main__':
    camera_lock=Lock()

    flask_process = Process(target=run_flask)
    export_process = Process(target=export)
    camera_process = Process(target=camera_control)

    # Start both processes
    flask_process.start()
    camera_process.start()
    export_process.start()

    # Wait for both processes to finish (this won't happen since both run indefinitely)
    flask_process.join()
    export_process.join()
    camera_process.join()

# from website import create_app  
    
# app = create_app()
# def run_flask():
#     app.run(host='0.0.0.0', port=8888, debug=True)

# if __name__ == '__main__':
#     run_flask()