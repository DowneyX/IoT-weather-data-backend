from datetime import datetime

from sqlalchemy import String
from app import db

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer(), primary_key=True)
    device_id = db.Column(String(40), nullable=False)
    temperature = db.Column(db.Float(), nullable=False)
    humidity = db.Column(db.Float(), nullable=False)
    pressure = db.Column(db.Float(), nullable=False)
    has_send = db.Column(db.Boolean(), nullable=False)
    measured_at = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=True)
    deleted_at = db.Column(db.DateTime(), nullable=True)
