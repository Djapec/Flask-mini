from flask import request
from flask_restplus import Resource
from marshmallow import ValidationError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from flask_app import db
from flask_app.measurement import measurements_api
from flask_app.measurement.models import Measurement
from sqlalchemy.exc import SQLAlchemyError
from flask_app.measurement.schemas import MeasurementGet, MeasurementPost

# dek
# table +
# status codes


Measurement_get = MeasurementGet()
Measurement_post = MeasurementPost()

# blueprint level error handler flask

@measurements_api.route('/')
@measurements_api.route('/<int:measurement_id>')
class MeasurementApi(Resource):
    def post(self):
        try:
            measurement_dict = Measurement_post.load(request.get_json(force=True))
            measurement = Measurement(
                temperature=measurement_dict['temperature'],
                air_quality=measurement_dict['air_quality'],
                humidity=measurement_dict['humidity'])


            db.session.add(measurement)
            db.session.commit()

        except SQLAlchemyError as sqlalchemy_error:
            print(f"SqlAlchemy error:: {sqlalchemy_error}")
            return {'message': 'Database error.'}, 500

        except ValidationError as validationError:
            print(f"Validation error:: {validationError}")
            return {'message': F'Validation error :D{validationError}'}, 500

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
                         'humidity': measurement.humidity}

        return Measurement_get.dump(response_data), 200
