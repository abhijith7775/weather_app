from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

app = Flask(__name__)

# Get API key
API_KEY = os.getenv("WEATHER_API_KEY")

# OpenWeather API URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/weather")
def weather():

    city = request.args.get("city")

    if not city:
        return jsonify({
            "error": "Please provide a city"
        }), 400

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 404:
        return jsonify({
            "error": "City not found"
        }), 404

    if response.status_code != 200:
        return jsonify({
            "error": "Weather API request failed",
            "status_code": response.status_code,
            "details": response.text
        }), response.status_code

    data = response.json()

    # Select only the data our application needs
    weather_data = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "weather_main": data["weather"][0]["main"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"],
        "visibility": data["visibility"]
    }

    return jsonify(weather_data)


if __name__ == "__main__":
    app.run(debug=True)