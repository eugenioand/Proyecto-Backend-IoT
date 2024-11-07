
from flask import Flask
from db import db
from flask_marshmallow import Marshmallow
from app.utils.error.error_handlers import register_error_handlers, setup_jwt_handlers
from app.routes.central_routes import register_blueprints
from flask import Flask
from db import db
from decouple import config
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS

env = config('FLASK_ENV', 'development')

app = Flask(__name__)

def init_app(config):
   
    # Configuration
    app.config.from_object(config)
    db.init_app(app)
    ma = Marshmallow(app)
    jwt = JWTManager(app)

    
    if env == 'development':
        CORS(app, resources={r"/*": {"origins": "https://proyecto-front-end-iot.vercel.app/"}})
    elif env == 'production':
        CORS(app, resources={r"/*": {"origins": "https://wetlandmanager.vercel.app/"}})

    setup_jwt_handlers(jwt)

    # Synchronize changes between models and tables
    """ with app.app_context():
        db.create_all()
     """
    swagger = Swagger(app)
    register_blueprints(app)
    #app.register_blueprint(user_bp)
    # Registrar los manejadores de errores
    register_error_handlers(app)  # Aquí se usan los manejadores de errores

    
    """ if __name__ == "__main__":
        app.run(debug=True) """
    
    return app
