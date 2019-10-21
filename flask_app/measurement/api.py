from flask import request
from flask_restplus import Resource
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from flask_app import db
from flask_app.measurement import measurements_api
from flask_app.measurement.models import Measurement
from sqlalchemy.exc import SQLAlchemyError


@measurements_api.route('/')
@measurements_api.route('/<int:measurement_id>')
class MeasurementApi(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)

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

    def get(self, measurement_id):
        try:
            measurement = db.session. \
                query(Measurement). \
                filter(Measurement.id == measurement_id). \
                one()

        except NoResultFound as error:
            print(f"No result found for id: {measurement_id}")
            print(f"Error: {error}")
            return {'message': 'No result found.'}, 404
        except MultipleResultsFound as error:
            print(f"Multiple results found for id: {measurement_id}")
            print(f"Error: {error}")
            return {'message': 'Database error.'}, 500
        except SQLAlchemyError as sqlalchemy_error:
            print(f"SqlAlchemy error:: {sqlalchemy_error}")
            return {'message': 'Database error.'}, 500
        except Exception as server_error:
            print(f"Server error:: {server_error}")
            return {'message': 'Server error.'}, 500

        response_data = {'temperature': measurement.temperature,
                         'air_quality': measurement.air_quality,
                         'humiidity': measurement.humidity,
                         'created_at': measurement.created_datetime}

        return response_data, 200

