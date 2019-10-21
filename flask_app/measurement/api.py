from flask import request
from flask_restplus import Resource

from flask_app import db
from flask_app.measurement import measurements_api
from flask_app.measurement.models import Measurement
from sqlalchemy.exc import SQLAlchemyError


@measurements_api.route('/')
class MeasurementApi(Resource):
    def post(self):
        try:
            data = request.frmo_json(force=True)

            measurement = Measurement(
                temperature=data['temperature'],
                air_quality=data['air_quality'],
                humidity=data['humidity'])

            db.session.add(measurement)
            db.session.commit()
        except SQLAlchemyError as sqlalchemy_error:
            print(f"SqlAlchemy error:: {sqlalchemy_error}")
            return {'message': 'Database error.'}, 500
        except Exception as error:
            print(f"Unknown error:: {error}")
            return {'message': 'Unknown error.'}, 500

        return {'message': 'Success!'}, 200

