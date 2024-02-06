from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def fetch_weather_data(api_key, lat, lon):
    """
    Fetches weather data from the OpenWeatherMap API.

    Parameters:
        api_key (str): The API key for accessing the OpenWeatherMap API.
        lat (float): The latitude coordinate.
        lon (float): The longitude coordinate.

    Returns:
        dict or None: The weather data if successfully fetched, or None if an error occurred.
    """
    url = f"https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lon}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        if 'message' in data:
            print(f"Error: {data['message']}")
            return None
        return data
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return None

def validate_coordinates(lat, lon):
    """
    Validates latitude and longitude coordinates.

    Parameters:
        lat (str): The latitude coordinate input by the user.
        lon (str): The longitude coordinate input by the user.

    Returns:
        tuple: A tuple containing the validated latitude and longitude as floats, or (None, None) if invalid inputs.
    """
    try:
        lat = float(lat)
        lon = float(lon)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        else:
            print("Invalid latitude or longitude. Latitude must be between -90 and 90, and longitude between -180 and 180.")
            return None, None
    except ValueError:
        print("Latitude and longitude must be numeric values.")
        return None, None

@app.route("/weather", methods=["GET"])
def get_weather_data():
    """
    Main function of the program.
    Prompts the user for latitude and longitude coordinates, fetches weather data, and prints the result.
    """
    api_key = "78d6507e36c0f4d824cb206fface4135"
    lat_input = request.args.get("lat")
    lon_input = request.args.get("lon")
    lat, lon = validate_coordinates(lat_input, lon_input)
    if lat is not None and lon is not None:
        weather_data = fetch_weather_data(api_key, lat, lon)
        if weather_data:
            return jsonify(weather_data)
        else:
            return "Failed to fetch weather data.", 500
    else:
        return "Invalid latitude or longitude inputs.", 400

if __name__ == "__main__":
    app.run(debug=True)
