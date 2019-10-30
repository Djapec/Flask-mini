import math
from datetime import datetime

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


@measurements_api.route('/history/<int:start>/<int:end>/<int:limit>')
class MeasurementApi2(Resource):
    def get(self, start, end, limit):

        # if type(limit) is str:
        #     print("True")
        # else:
        #     print("no")

        start_date = datetime.fromtimestamp(start / 1000)
        end_date = datetime.fromtimestamp(end / 1000)
        limit_date = limit

        measurement_history = db.session. \
            query(Measurement). \
            filter(Measurement.created_datetime >= start_date, Measurement.created_datetime <= end_date)

        list_pom = []

        len = measurement_history.count()

        if limit_date != 0:
            step = math.ceil(len / limit_date)
        else:
            step = 1

        for i in range(0, len, step):
            list_pom.append(Measurement_get.dump(measurement_history[i]))

        return {"Measurements": list_pom}, 200


@measurements_api.route('/latest')
class MeasurementApi3(Resource):
    def get(self):
        measurement_latest = db.session.query(Measurement).order_by(Measurement.id.desc()).first()

        return Measurement_get.dump(measurement_latest)
