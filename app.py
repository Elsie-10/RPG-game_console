import os 
from flask import Flask
from flask_cors import CORS
from config import config 
from flask import render_template
from Routes.game_routes import game_bp
from Routes.player_routes import player_bp
from Routes.command_routes import command_bp



def create_app(config_name=None):
    #create a flask app instance
    app = Flask(__name__) # __name__ flask uses it to locate template or static files.
    app.config.from_object(config[config_name or 'default']) # .from_object()to actually load the configuration
    #intialize CORS on the app
    CORS(app) # security prevents other websites from making unauthorized request to your api

    # Inside create_app(), after CORS(app)
    app.template_folder = 'templates'  # Folder for HTML templates
    app.static_folder = 'static'       # Folder for CSS/JS files

    
    app.register_blueprint(game_bp, url_prefix='/api')
    app.register_blueprint(player_bp, url_prefix='/api')
    app.register_blueprint(command_bp, url_prefix='/api')

    
    @app.route('/')
    def home():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()