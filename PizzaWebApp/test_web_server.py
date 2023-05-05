import os 
from pizza_web_app import app 

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT','5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST,PORT,debug=True)