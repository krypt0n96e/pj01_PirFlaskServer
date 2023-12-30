from website import create_app 

app = create_app()
def run_flask():
    app.run(host='0.0.0.0', port=8888, debug=False)