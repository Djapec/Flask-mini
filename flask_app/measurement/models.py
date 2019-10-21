from datetime import datetime
from flask_app import db
from sqlalchemy import Column, Integer, DateTime


class Measurement(db.Model):

    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    temperature = Column(Integer, nullable=False)
    air_quality = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    created_datetime = Column(DateTime, nullable=False, default=datetime.now)