import os 
from waitress import serve
from pizza_web_app import app 

testing = 0

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    if testing == 1:
        PORT = 5555
        app.run(HOST,PORT,debug=True)
    else:
        PORT = 80
        serve(app,host=HOST,port=PORT,threads=1)