# from multiprocessing import Process
# from flaskServer import run_flask
# from task2 import export

# if __name__ == '__main__':
#     flask_process = Process(target=run_flask)
#     export_process = Process(target=export)

#     # Start both processes
#     flask_process.start()
#     export_process.start()

#     # Wait for both processes to finish (this won't happen since both run indefinitely)
#     flask_process.join()
#     export_process.join()

from website import create_app  
    
app = create_app()
def run_flask():
    app.run(host='0.0.0.0', port=8888, debug=True)

if __name__ == '__main__':
    run_flask()