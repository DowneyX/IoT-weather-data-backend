from datetime import date, datetime
from flask import Blueprint, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required
from .. import db
from ..models.WeatherData import WeatherData
import json

weather_data_api = Blueprint('weather_data_api', __name__)


@weather_data_api.route('/post', methods=['POST'])
def weatherData_post():
    data = request.get_json(force=True)
    if (not "device_id" in data):
        return "bad request", 400
    if (not "measured_at" in data):
        return "bad request", 400
    if (not "temperature" in data):
        return "bad request", 400
    if (not "pressure" in data):
        return "bad request", 400
    if (not "humidity" in data):
        return "bad request", 400

    data_obj = WeatherData(
        temperature=data["temperature"],
        pressure=data["pressure"],
        humidity=data["humidity"],
        measured_at=datetime.strptime(
            data["measured_at"], "%d/%m/%Y, %H:%M:%S"),
        has_send=False,
        created_at=datetime.now()
    )
    db.session.add(data_obj)
    db.session.commit()

    return "data comitted"


@weather_data_api.route('/get/<date>', methods=['GET'])
def weather_data_get_date(date):

    if not is_date(date):
        return "Bad request", 400

    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        # Calculate the start and end datetime objects for the specified day
        start_datetime = datetime.combine(date_obj.date(), datetime.min.time())
        end_datetime = datetime.combine(date_obj.date(), datetime.max.time())

        # Query the database for weather data within the date range
        weather_data = WeatherData.query.filter(
            WeatherData.measured_at >= start_datetime,
            WeatherData.measured_at <= end_datetime
        ).all()

        # Convert the queried data to JSON response or return an appropriate response
        if weather_data:
            data_as_dicts = [
                {
                    'id': data.id,
                    'has_send': data.has_send,
                    'measured_at': data.measured_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'temperature': data.temperature,
                    'humidity': data.humidity,
                    'pressure': data.pressure
                }
                for data in weather_data
            ]
            return jsonify(data_as_dicts)
        else:
            return "No data found for the specified date.", 404
    except ValueError:
        return "Bad request", 400


@weather_data_api.route('/get/not-send/', methods=['GET'])
def weather_data_get_not_send():
    filtered_data = WeatherData.query.filter(WeatherData.has_send == False)
    weather_data = filtered_data.limit(1000).all()

    if weather_data:
        data_as_dicts = [
            {
                'id': data.id,
                'has_send': data.has_send,
                'measured_at': data.measured_at.strftime("%Y-%m-%d %H:%M:%S"),
                'temperature': data.temperature,
                'humidity': data.humidity,
                'pressure': data.pressure
            }
            for data in weather_data
        ]
        return jsonify(data_as_dicts)
    else:
        return "No unsend data.", 404


def is_date(date_str):

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
