from flask import Flask
from flasgger import Swagger
from .config import Config, TestConfig
# from flask_cors import CORS
from .extensions import db, migrate
from .blueprints.tasks.routes import tasks_blueprint
from .blueprints.auth.routes import auth_blueprint

swagger_template = {
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "auth",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    }
}

def app_():
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    # app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
        with db.engine.connect() as connection:
            if not connection.closed: print("✅ Connected to PostgresSql DB")
            else: print("❌ Failed connected to PostgresSql DB")

    # CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(tasks_blueprint)
    app.register_blueprint(auth_blueprint)

    Swagger(app, template=swagger_template)

    return app
