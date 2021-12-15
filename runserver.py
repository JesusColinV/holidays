"""
This script runs the python_webapp_flask application using a development server.
"""

#from werkzeug.middleware.dispatcher import DispatcherMiddleware 
#from werkzeug.serving import run_simple

from os import environ
from modules.server import server

from admi_dash.app_admin  import app 


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8095'))
    except ValueError:
        PORT = 8095
    
    #run_simple(HOST, port=PORT, application=DispatcherMiddleware(server))
    server.run(HOST, PORT)