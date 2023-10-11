from datetime import datetime
from .. import db


class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer(), primary_key=True)
    temperature = db.Column(db.Float(), nullable=False)
    humidity = db.Column(db.Float(), nullable=False)
    pressure = db.Column(db.Float(), nullable=False)
    has_send = db.Column(db.Boolean(), nullable=False)
    measured_at = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=True)
    deleted_at = db.Column(db.DateTime(), nullable=True)
