import os 
from flask import Flask
from flask_cors import CORS
from config import config 

def create_app(config_name=None):
    #create a flask app instance
    app = Flask(__name__) # __name__ flask uses it to locate template or static files.
    app.config.from_object(config[config_name or 'default']) # .from_object()to actually load the configuration
    #intialize CORS on the app
    CORS(app) # security prevents other websites from making unauthorized request to your api
    
    @app.route('/')
    def home():
        return{"message":"Welcome to the RPG Fantacy Game."}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()