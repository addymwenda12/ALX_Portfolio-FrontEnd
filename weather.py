from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

def fetch_weather_data(api_key, city_name):
    """
    Fetches weather data from the OpenWeatherMap API.

    Parameters:
        api_key (str): The API key for accessing the OpenWeatherMap API.
        city_name (str): The name of the city.

    Returns:
        dict or None: The weather data if successfully fetched, or None if an error occurred.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return None

@app.route("/weather", methods=["GET"])
def get_weather_data():
    """
    Main function of the program.
    Prompts the user for the city name, fetches weather data, and returns the result as JSON.
    """
    api_key = "78d6507e36c0f4d824cb206fface4135"
    city_name = request.args.get("city")
    if city_name:
        weather_data = fetch_weather_data(api_key, city_name)
        if weather_data:
            return jsonify(weather_data)
        else:
            return jsonify({"error": "Failed to fetch weather data."}), 500
    else:
        return jsonify({"error": "City name is missing."}), 400

@app.route("/")
def home():
    """
    Serve the index.html file
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
