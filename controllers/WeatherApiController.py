from datetime import date, datetime
from flask import Blueprint, flash, redirect, render_template, url_for, request, jsonify
from sqlalchemy import false, true
from models.WeatherData import WeatherData
import json
from app import db
import joblib

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
        device_id=data["device_id"],
        measured_at=datetime.strptime(
            data["measured_at"], "%d/%m/%Y, %H:%M:%S"),
        has_send=False,
        created_at=datetime.now()
    )
    db.session.add(data_obj)
    db.session.commit()

    return "data comitted"

@weather_data_api.route('/put/is-send/<id>', methods=['PUT'])
def weatherData_put(id):
    
    data_obj = WeatherData.query.filter_by(id=id).first()
    
    if not data_obj:
        return "bad request", 400

    data_obj.has_send = True
    db.session.commit()

    return "dataUpdated"


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
                    'pressure': data.pressure,
                    'device_id': data.device_id
                }
                for data in weather_data
            ]
            return jsonify(data_as_dicts)
        else:
            data_as_dicts =[{}]
            return jsonify(data_as_dicts)
    except ValueError:
        return "Bad request", 400

@weather_data_api.route('/get/not-send/', methods=['GET'])
def weather_data_get_not_send():
    filtered_data = WeatherData.query.filter(WeatherData.has_send == False)
    weather_data = filtered_data.limit(1).all()

    if weather_data:
        data_as_dicts = [
            {
                'id': data.id,
                'has_send': data.has_send,
                'measured_at': data.measured_at.strftime("%Y-%m-%d %H:%M:%S"),
                'temperature': data.temperature,
                'humidity': data.humidity,
                'pressure': data.pressure,
                'device_id': data.device_id
 
            }
            for data in weather_data
        ]
        return jsonify(data_as_dicts)
    else:
        return jsonify([{}])

@weather_data_api.route('/get/latest/', methods=['GET'])
def weather_data_get_latest():
    weather_data = WeatherData.query.order_by(WeatherData.measured_at.desc()).limit(1)
    if weather_data:
        data_as_dicts = [
            {
                'id': data.id,
                'has_send': data.has_send,
                'measured_at': data.measured_at.strftime("%Y-%m-%d %H:%M:%S"),
                'temperature': data.temperature,
                'humidity': data.humidity,
                'pressure': data.pressure,
                'device_id': data.device_id
 
            }
            for data in weather_data
        ]
        return jsonify(data_as_dicts)
    else:
        return "No unsend data.", 404

@weather_data_api.route('/get/rain-prediction/', methods=['GET'])
def weather_data_get_rain_prediction():
    weather_data = WeatherData.query.order_by(WeatherData.measured_at.desc()).limit(1)
    if weather_data:

        # Load the pre-trained model
        loaded_model = joblib.load('weather_predictor.pkl')

        # Create a DataFrame with a single row of data
        new_data = [[0.74],[10.5],[999.1]] 
    
        # Make prediction using the loaded model
        prediction = loaded_model.predict(new_data)
        result = prediction[0]
    
        output = False
        if result > 0:
            output = true
    
        data_as_dicts = [{
            "prediction": output
        }]
        return jsonify(data_as_dicts) 
    else:
        return "No unsend data.", 404



def is_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
