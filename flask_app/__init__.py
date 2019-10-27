from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()

from flask_app.measurement.models import Measurement
from flask_app.measurement import measurement_blueprint


def createApp(config):  # main()

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(measurement_blueprint)

    return app