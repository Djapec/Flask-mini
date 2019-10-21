from flask_app.__init__ import db
from server import app
from flask_app.measurement.models import Measurement
import random

def insert_measurement_data():
    for i in range(1, 1000):
        new_model = Measurement(
        temperature=random.randint(1, 100),
        air_quality=random.randint(1, 100),
        humidity=random.randint(1, 100)
        )
        db.session.add(new_model)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        try:
            #insert_measurement_data()
            test = Measurement.query.all()
            print(test[2].created_datetime)
        except Exception as e:
            print(e)