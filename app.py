from flask import Flask
# from flask_migrate import Migrate

from config.development import Development


def createApp(config):
    app = Flask(__name__)
    app.config.from_object(config)

    return app




